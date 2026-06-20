import os
import time
import random
from datetime import datetime, timezone
from website import create_app, db
from website.models import AffiliateLink
from website.seo_utils import download_and_cache_image

from dotenv import load_dotenv

load_dotenv()

# =========================================================================
# OFFICIAL AMAZON PA-API 5.0 INTEGRATION
# =========================================================================
def fetch_amazon_data(asin):
    print(f"Pinging Amazon Creators API for ASIN: {asin}...")
    
    # Lazy load to avoid import errors if package is missing
    try:
        from amazon_creatorsapi import AmazonCreatorsApi
    except ImportError:
        raise ImportError("Please run: pip install python-amazon-paapi")
        
    client_id = os.getenv('AMAZON_CLIENT_ID')
    client_secret = os.getenv('AMAZON_CLIENT_SECRET')
    partner_tag = os.getenv('AMAZON_PARTNER_TAG')
    country = os.getenv('AMAZON_COUNTRY', 'US')
    
    if not all([client_id, client_secret, partner_tag]):
        raise ValueError("Missing Amazon Creators API credentials in .env file (AMAZON_CLIENT_ID, AMAZON_CLIENT_SECRET, AMAZON_PARTNER_TAG)")

    api_version = "3.1" if client_secret.startswith("amzn1.oa2-cs.v1.") else "2.2"
    
    amazon = AmazonCreatorsApi(
        credential_id=client_id,
        credential_secret=client_secret,
        version=api_version,
        tag=partner_tag,
        country=country
    )
    
    try:
        items = amazon.get_items([asin])
        if not items:
            print(f"[X] No item found for ASIN: {asin}")
            return {
                "is_available": False, "current_price": None, 
                "original_price": None, "discount_percentage": None, 
                "product_title": None
            }
            
        item = items[0]
        
        is_available = False
        current_price = None
        original_price = None
        discount_percentage = None
        
        if item.offers and item.offers.listings:
            listing = item.offers.listings[0]
            # Consider 'Now' or 'Preorder' or anything with a price as available
            if listing.price and listing.price.amount:
                is_available = True
                current_price = listing.price.amount
                if hasattr(listing, 'saving_basis') and listing.saving_basis:
                    original_price = listing.saving_basis.amount
                    try:
                        discount_percentage = int(((original_price - current_price) / original_price) * 100)
                    except:
                        discount_percentage = 0
                else:
                    original_price = current_price
                    discount_percentage = 0
                    
        title = item.item_info.title.display_value if (hasattr(item, 'item_info') and item.item_info and item.item_info.title) else f"Amazon Product {asin}"
        
        image_url = None
        if hasattr(item, 'images') and item.images and item.images.primary and item.images.primary.large:
            image_url = item.images.primary.large.url
            
        features = []
        if hasattr(item, 'item_info') and item.item_info and item.item_info.features and item.item_info.features.display_values:
            features = item.item_info.features.display_values
                    
        return {
            "is_available": is_available,
            "current_price": round(current_price, 2) if current_price else None,
            "original_price": round(original_price, 2) if original_price else None,
            "discount_percentage": discount_percentage,
            "product_title": title,
            "image_url": image_url,
            "features": features
        }
    except Exception as e:
        print(f"[X] Amazon Creators API Error for {asin}: {e}")
        return {
            "is_available": False,
            "current_price": None,
            "original_price": None,
            "discount_percentage": None,
            "product_title": None,
            "image_url": None,
            "features": []
        }

def sync_all_links():
    app = create_app()
    with app.app_context():
        # Get all links that have an ASIN assigned
        links = AffiliateLink.query.filter(AffiliateLink.asin.isnot(None), AffiliateLink.asin != '').all()
        
        print(f"Found {len(links)} products to sync.")
        for link in links:
            try:
                data = fetch_amazon_data(link.asin)
                link.is_available = data['is_available']
                link.current_price = data['current_price']
                link.original_price = data['original_price']
                link.discount_percentage = data['discount_percentage']
                
                if data['image_url']:
                    link.image_url = download_and_cache_image(data['image_url'], keyword=link.product_title)
                    
                if data['features']:
                    link.features_json = data['features']
                    
                # Update price history (keep last 30 data points)
                if data['current_price']:
                    history = link.price_history or []
                    # Append today's price
                    history.append({
                        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                        "price": data['current_price']
                    })
                    link.price_history = history[-30:]
                
                # Only update title if the API returns one and the user hasn't hardcoded one
                if data['product_title'] and not link.product_title:
                    link.product_title = data['product_title']
                    
                link.last_synced_at = datetime.now(timezone.utc)
                db.session.commit()
                if not link.is_available:
                    print(f"[\u2713] Synced {link.slug}: OUT OF STOCK")
                else:
                    print(f"[\u2713] Synced {link.slug}: ${link.current_price} ({link.discount_percentage}% off)")
            except Exception as e:
                print(f"[X] Error syncing {link.slug}: {e}")
                db.session.rollback()

if __name__ == "__main__":
    print(f"Starting scheduled Amazon sync at {datetime.now()}...")
    sync_all_links()
    print("Sync complete.")
