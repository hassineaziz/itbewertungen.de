import sys
import os
from datetime import datetime, timezone
from website import create_app, db
from website.models import BlogPost

app = create_app()

def seed_custom_posts():
    posts_data = [
        # 1. 2 Products (Comparison Template)
        {
            "title": "Sony WH-1000XM5 vs. Bose QuietComfort Ultra: Kopfhörer-Vergleich (2026)",
            "slug": "sony-wh1000xm5-vs-bose-qc-ultra-vergleich-2026",
            "excerpt": "Zwei absolute Giganten des Active Noise Canceling treten gegeneinander an. Welcher Kopfhörer bietet den besten Klang und den höchsten Tragekomfort im Zug oder Flugzeug?",
            "template": "affiliate_comparison_template",
            "tags": ["audio", "headset", "featured"],
            "cover_image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=1600&q=80",
            "structured_content": {
                "headline": "Sony WH-1000XM5 vs. Bose QuietComfort Ultra: Kopfhörer-Vergleich (2026)",
                "sub_head": "Zwei absolute Giganten des Active Noise Canceling treten gegeneinander an. Welcher Kopfhörer bietet den besten Klang, den höchsten Tragekomfort und die tiefste Stille im Zug oder Flugzeug? Wir haben beide Modelle wochenlang im Labor und Alltag getestet.",
                "products": [
                    {
                        "rank": 1,
                        "name": "Sony WH-1000XM5 Wireless ANC",
                        "badge": "Bester Allrounder & Sound",
                        "price": "329,00 €",
                        "rating": 9.8,
                        "affiliate_slug": "sony-wh-1000xm5",
                        "image_url": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=400&q=80",
                        "summary": "Der Sony WH-1000XM5 überzeugt durch eine phänomenale Akkulaufzeit, smarte Steuerung per App und ein extrem ausgewogenes, detailreiches Klangbild mit hervorragender Räumlichkeit.",
                        "pros": [
                            "Herausragender detailreicher Klang",
                            "Smarte Speak-to-Chat Funktion",
                            "30 Stunden Akkulaufzeit mit ANC"
                        ],
                        "cons": [
                            "Nicht faltbar (nur flach drehbar)",
                            "Touch-Steuerung bei Kälte träge"
                        ],
                        "specs": [
                            "Akkulaufzeit: 30 Std. (mit ANC)",
                            "Bluetooth-Codecs: LDAC, AAC, SBC",
                            "Treibergröße: 30 mm",
                            "Gewicht: 250 g"
                        ]
                    },
                    {
                        "rank": 2,
                        "name": "Bose QuietComfort Ultra",
                        "badge": "Bestes ANC & Komfort",
                        "price": "379,00 €",
                        "rating": 9.6,
                        "affiliate_slug": "bose-qc-ultra",
                        "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=400&q=80",
                        "summary": "Bose setzt mit dem QC Ultra neue Maßstäbe beim Active Noise Canceling und beim Tragekomfort. Perfekt für lange Flüge dank des genialen Faltmechanismus.",
                        "pros": [
                            "Branchenführendes Noise Canceling",
                            "Immersives 3D-Audio integriert",
                            "Sehr kompakter Faltmechanismus"
                        ],
                        "cons": [
                            "Akkulaufzeit etwas kürzer (24h)",
                            "Kein Multipoint bei LDAC"
                        ],
                        "specs": [
                            "Akkulaufzeit: 24 Std. (mit ANC)",
                            "Bluetooth-Codecs: aptX Adaptive, AAC",
                            "Trageform: Over-Ear, faltbar",
                            "Gewicht: 252 g"
                        ]
                    }
                ],
                "buying_guide": "### Worauf Sie beim Kauf von ANC-Kopfhörern achten sollten\n\n#### 1. Active Noise Canceling (Aktive Geräuschunterdrückung)\nDie wichtigste Funktion moderner Premium-Kopfhörer ist die Fähigkeit, Außengeräusche wegzufiltern. Während Sony auf ein System mit acht Mikrofonen und zwei Prozessoren setzt, um hohe Frequenzen und Stimmen besonders gut zu isolieren, konzentriert sich Bose auf die schiere Tiefe des Bassrauschens (wie Triebwerkslärm im Flugzeug). Beide Hersteller bieten hervorragende Transparenz-Modi, die Außengeräusche natürlich durchleiten.\n\n#### 2. Tragekomfort und Ergonomie\nDa Kopfhörer oft stundenlang getragen werden, ist der Komfort entscheidend. Bose verwendet weichere Ohrpolster und einen ausgewogenen Anpressdruck, was vor allem Brillenträgern entgegenkommt. Der Sony WH-1000XM5 hat einen schlankeren Kopfbügel, lässt sich jedoch im Gegensatz zum Bose QC Ultra nicht mehr zusammenfalten, was mehr Platz im Handgepäck beansprucht.\n\n#### 3. Bluetooth-Codecs und Klangqualität\nWer hochauflösende Musik (High-Res Audio) streamen möchte, muss auf die unterstützten Codecs achten. Sony bietet mit LDAC eine extrem hohe Bitrate auf Android-Geräten. Bose kontert mit Qualcomms aptX Adaptive, was besonders geringe Latenzen beim Gaming oder Filmschauen garantiert. Beide Modelle klingen fantastisch, wobei Sony etwas neutraler und Bose eher spaßbetont mit kräftigem Bass abgestimmt ist.",
                "faq": [
                    {
                        "question": "Kann man die Kopfhörer auch mit Kabel nutzen?",
                        "answer": "Ja, beide Modelle verfügen über einen Klinkenanschluss (3.5 mm bei Sony, 2.5 mm bei Bose) und ein passendes Audiokabel wird im Lieferumfang mitgeliefert."
                    },
                    {
                        "question": "Unterstützen beide Modelle Bluetooth Multipoint?",
                        "answer": "Ja, sowohl der Sony WH-1000XM5 als auch der Bose QC Ultra können sich mit zwei Geräten (z.B. Smartphone und Laptop) gleichzeitig verbinden und nahtlos umschalten."
                    },
                    {
                        "question": "Wie lange dauert das Aufladen?",
                        "answer": "Der Sony WH-1000XM5 lädt in ca. 3 Stunden vollständig auf (3 Minuten Laden bringt 3 Stunden Laufzeit). Der Bose QC Ultra benötigt ca. 2 Stunden für eine vollständige Ladung."
                    },
                    {
                        "question": "Sind die Kopfhörer spritzwassergeschützt?",
                        "answer": "Weder Sony noch Bose zertifizieren diese Over-Ear-Modelle mit einer offiziellen IPX-Schutzklasse. Sie sollten daher nicht bei starkem Regen oder intensivem Sport getragen werden."
                    },
                    {
                        "question": "Kann man das ANC komplett ausschalten?",
                        "answer": "Ja, in den jeweiligen Apps (Sony Headphones Connect und Bose Music App) lässt sich das Noise Canceling deaktivieren oder in verschiedenen Stufen anpassen."
                    }
                ],
                "verdict": "Wer den absolut feinsten Klang und die umfangreichste App-Konfiguration wünscht, greift zum Sony WH-1000XM5. Für Vielreisende, die den besten Tragekomfort und ein faltbares Design benötigen, ist der Bose QuietComfort Ultra die erste Wahl."
            }
        },
        # 2. 3 Products (Best X For Y Template)
        {
            "title": "Die 3 besten mechanischen Tastaturen für Programmierer (2026)",
            "slug": "die-3-besten-mechanischen-tastaturen-programmierer-2026",
            "excerpt": "Lange Code-Sessions erfordern ein erstklassiges Tippgefühl. Wir vergleichen die drei besten mechanischen Tastaturen für Office und Entwicklung.",
            "template": "best_x_for_y_template",
            "tags": ["office", "keyboard", "featured"],
            "cover_image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=1600&q=80",
            "structured_content": {
                "headline": "Die 3 besten mechanischen Tastaturen für Programmierer (2026)",
                "sub_head": "Lange Code-Sessions und endlose E-Mails erfordern die beste Tastatur. Mechanische Tastaturen bieten nicht nur ein unvergleichbares Tippgefühl, sondern schonen auch die Handgelenke und steigern die Produktivität. Wir vergleichen die 3 Top-Modelle.",
                "picks": [
                    {
                        "rank": 1,
                        "name": "Keychron Q1 Pro QMK/VIA",
                        "badge": "Testsieger & Beste Qualität",
                        "price": "219,00 €",
                        "rating": 9.8,
                        "affiliate_slug": "keychron-q1-pro",
                        "image_url": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?auto=format&fit=crop&w=400&q=80",
                        "summary": "Das absolute Nonplusultra für Keyboard-Enthusiasten. Vollaluminium-Gehäuse, gasket-mounted Aufbau für einen gedämpften Klang und vollständige VIA-Programmierbarkeit.",
                        "pros": [
                            "Vollaluminium-Gehäuse in Studio-Qualität",
                            "Kabellos über Bluetooth 5.1",
                            "Vollständig programmierbar mit QMK/VIA"
                        ],
                        "cons": [
                            "Sehr schwer (ca. 1,7 kg)",
                            "Kein USB-Dongle im Lieferumfang"
                        ],
                        "specs": [
                            "Layout: 75% TKL Layout",
                            "Gehäuse: CNC-Aluminium",
                            "Switches: Keychron K Pro",
                            "Konnektivität: BT 5.1 / USB-C"
                        ]
                    },
                    {
                        "rank": 2,
                        "name": "NuPhy Air75 V2 Low-Profile",
                        "badge": "Beste flache Tastatur",
                        "price": "149,00 €",
                        "rating": 9.5,
                        "affiliate_slug": "nuphy-air75-v2",
                        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=400&q=80",
                        "summary": "Wer ein flaches Profil ähnlich dem Apple Magic Keyboard bevorzugt, aber das haptische Feedback mechanischer Switches will, findet mit der Air75 V2 das perfekte Schreibwerkzeug.",
                        "pros": [
                            "Ultradünnes Low-Profile-Design",
                            "1000Hz Polling-Rate im 2.4GHz Funk",
                            "Wunderbarer thockiger Klang ab Werk"
                        ],
                        "cons": [
                            "Akkulaufzeit mit RGB-Beleuchtung kurz",
                            "Standfüße etwas filigran"
                        ],
                        "specs": [
                            "Layout: 75% flaches Profil",
                            "Gehäuse: Alu-Rahmen & ABS",
                            "Switches: Gateron Low-Profile",
                            "Konnektivität: 2.4G / BT / USB"
                        ]
                    },
                    {
                        "rank": 3,
                        "name": "Logitech MX Mechanical",
                        "badge": "Bester Office-Allrounder",
                        "price": "169,00 €",
                        "rating": 9.1,
                        "affiliate_slug": "logitech-mx-mechanical",
                        "image_url": "https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=400&q=80",
                        "summary": "Die ideale Tastatur für alle, die bereits im Logitech MX-Ökosystem (MX Master Maus) arbeiten. Extrem zuverlässige Software, tolle Akkulaufzeit und nahtloser Multi-Device-Wechsel.",
                        "pros": [
                            "Monatelange Akkulaufzeit ohne RGB",
                            "Hervorragende Logi Options+ Software",
                            "Sehr leise Tactile-Quiet Switches"
                        ],
                        "cons": [
                            "Tastenkappen nicht standardmäßig tauschbar",
                            "Kein Hot-Swap-Support"
                        ],
                        "specs": [
                            "Layout: 100% Full-Size / TKL",
                            "Gehäuse: Alu-Topplate & ABS",
                            "Switches: Kailh Choc V2",
                            "Konnektivität: Logi Bolt / BT"
                        ]
                    }
                ],
                "buying_guide": "### Kaufberatung: Mechanische Tastaturen im Office-Einsatz\n\n#### 1. Welche Switches eignen sich für das Büro?\nDie Wahl der Schalter (Switches) bestimmt das Tippgefühl und die Lautstärke:\n- **Linear (Red):** Sehr leise und geschmeidig, gut für schnelles Tippen ohne Widerstand.\n- **Tactile (Brown):** Bieten einen spürbaren Druckpunkt beim Auslösen. Ideal fürs Schreiben, da man spürt, wann die Taste gedrückt wurde.\n- **Clicky (Blue):** Sehr laut und knackig. Im Großraumbüro absolut verboten, im Home-Office jedoch sehr beliebt.\n\n#### 2. Layouts und Ergonomie (75% vs. TKL vs. Full-Size)\nEntwickler bevorzugen oft kompakte Layouts wie 75% oder Tenkeyless (TKL), da die Hände näher beieinander liegen und der Weg zur Maus verkürzt wird. Full-Size-Tastaturen sind ideal für alle, die viele Zahlen in Excel eingeben müssen.\n\n#### 3. Software & Programmierbarkeit\nTastaturen mit QMK/VIA (wie die Keychron Q1 Pro) erlauben es, Tastenbelegungen und Makros direkt auf dem Chip der Tastatur zu speichern. Das funktioniert ohne lästige Hintergrundprogramme auf jedem Betriebssystem (Mac, Windows, Linux).",
                "faq": [
                    {
                        "question": "Was bedeutet Gasket Mount?",
                        "answer": "Gasket Mount beschreibt eine Bauweise, bei der die Tastaturplatte durch Dichtungsstreifen (Gaskets) im Gehäuse abgefedert gelagert ist. Dies sorgt für ein weicheres Tippgefühl und einen gedämpften, harmonischen Klang."
                    },
                    {
                        "question": "Funktionieren mechanische Tastaturen problemlos mit macOS?",
                        "answer": "Ja, die meisten modernen Tastaturen wie Keychron und NuPhy haben einen Schalter zum Wechseln des Layouts zwischen Mac und Windows und liefern passende Tastenkappen mit."
                    },
                    {
                        "question": "Was ist Hot-Swap?",
                        "answer": "Hot-Swap bedeutet, dass die mechanischen Switches ohne Löten aus der Platine gezogen und durch andere Modelle getauscht werden können. Perfekt zum Ausprobieren verschiedener Schalter."
                    },
                    {
                        "question": "Wie reinigt man eine mechanische Tastatur?",
                        "answer": "Mit einem Keycap-Puller zieht man die Tastenkappen ab und reinigt diese in Seifenwasser. Staub im Gehäuse kann mit Druckluft oder einem Pinsel entfernt werden."
                    },
                    {
                        "question": "Braucht man eine Handballenauflage?",
                        "answer": "Bei hohen Modellen (wie der Keychron Q1 Pro) wird eine Handballenauflage dringend empfohlen, um ein Überstrecken der Handgelenke zu verhindern. Bei Low-Profile Tastaturen ist das meist nicht nötig."
                    }
                ]
            }
        },
        # 3. 4 Products (Best X For Y Template)
        {
            "title": "Die 4 besten Actionkameras für Vlogger und Abenteurer (2026)",
            "slug": "die-4-besten-actionkameras-vlogger-abenteurer-2026",
            "excerpt": "Egal ob beim Downhill-Biken oder Vlogging in der Stadt – moderne Actionkameras müssen extrem stabilisiert sein. Wir vergleichen GoPro, DJI und Insta360.",
            "template": "best_x_for_y_template",
            "tags": ["camera", "video", "featured"],
            "cover_image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=1600&q=80",
            "structured_content": {
                "headline": "Die 4 besten Actionkameras für Vlogger und Abenteurer (2026)",
                "sub_head": "Egal ob beim Downhill-Biken, Tauchen oder Vlogging in der Stadt – moderne Actionkameras müssen extrem stabilisiert sein, auch bei wenig Licht gut filmen und einfach zu bedienen sein. Wir vergleichen die vier Top-Kameras des Jahres.",
                "picks": [
                    {
                        "rank": 1,
                        "name": "GoPro Hero 13 Black",
                        "badge": "Testsieger & Beste Bildqualität",
                        "price": "429,00 €",
                        "rating": 9.9,
                        "affiliate_slug": "gopro-hero-13",
                        "image_url": "https://images.unsplash.com/photo-1502920917128-1aa500764cbd?auto=format&fit=crop&w=400&q=80",
                        "summary": "Die unangefochtene Nummer Eins für höchste Bildauflösung und kreative Optionen. Mit 5.3K-Video, herausragender Stabilisierung und neuen magnetischen Filtern.",
                        "pros": [
                            "Hervorragendes 5.3K-Videobild",
                            "Herausragende HyperSmooth-Stabilisierung",
                            "Große Auswahl an Mod-Objektiven"
                        ],
                        "cons": [
                            "Wird bei 5.3K-Daueraufnahme heiß",
                            "Hoher Akkuverbrauch bei Kälte"
                        ],
                        "specs": [
                            "Auflösung: 5.3K bei 60 FPS",
                            "Sensor: 1/1.9 Zoll CMOS",
                            "Akku: 1900 mAh Enduro",
                            "Gewicht: 154 g"
                        ]
                    },
                    {
                        "rank": 2,
                        "name": "DJI Osmo Action 5 Pro",
                        "badge": "Beste für Low-Light & Akku",
                        "price": "379,00 €",
                        "rating": 9.7,
                        "affiliate_slug": "dji-osmo-action-5",
                        "image_url": "https://images.unsplash.com/photo-1564466809058-bf4114d55352?auto=format&fit=crop&w=400&q=80",
                        "summary": "DJI liefert mit der Action 5 Pro den besten Akku auf dem Markt und eine überragende Dynamic-Range bei schwierigen Lichtverhältnissen durch den brandneuen 4nm-Sensor.",
                        "pros": [
                            "Bis zu 4 Stunden Akkulaufzeit",
                            "Sehr gute Aufnahmen bei Dämmerung",
                            "Doppelte Touchscreens (vorne/hinten)"
                        ],
                        "cons": [
                            "Auflösung 'nur' auf 4K limitiert",
                            "Etwas wärmeres Farbprofil"
                        ],
                        "specs": [
                            "Auflösung: 4K bei 120 FPS",
                            "Sensor: 1/1.3 Zoll CMOS",
                            "Akku: 1950 mAh Extreme",
                            "Gewicht: 145 g"
                        ]
                    },
                    {
                        "rank": 3,
                        "name": "Insta360 Ace Pro 2",
                        "badge": "Beste für Vlogger",
                        "price": "449,00 €",
                        "rating": 9.4,
                        "affiliate_slug": "insta360-ace-pro-2",
                        "image_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?auto=format&fit=crop&w=400&q=80",
                        "summary": "Ausgestattet mit einem klappbaren Touchscreen ist die Ace Pro 2 die perfekte Kamera für Vlogger. Die Leica-Optik liefert knackige Farben und tollen Kontrast.",
                        "pros": [
                            "Praktischer 2.4-Zoll Klappbildschirm",
                            "Leica-Farben direkt aus der Kamera",
                            "8K-Zeitraffer & KI-Assistent"
                        ],
                        "cons": [
                            "Größer und schwerer als GoPro",
                            "Mindestabstand für Fokus relativ hoch"
                        ],
                        "specs": [
                            "Auflösung: 8K bei 30 FPS",
                            "Sensor: 1/1.3 Zoll CMOS",
                            "Akku: 1800 mAh Schnellladung",
                            "Gewicht: 179 g"
                        ]
                    },
                    {
                        "rank": 4,
                        "name": "GoPro Hero 11 Black Mini",
                        "badge": "Beste Kompaktkamera",
                        "price": "249,00 €",
                        "rating": 8.8,
                        "affiliate_slug": "gopro-hero-11-mini",
                        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=400&q=80",
                        "summary": "Die ideale Kamera zur Helmmontage. Sie verzichtet auf Displays, um maximale Robustheit und ein extrem leichtes Gehäuse zu bieten.",
                        "pros": [
                            "Sehr kompakt und leicht",
                            "Gleiche Videoqualität wie Hero 11 Black",
                            "Zweites Befestigungs-Setup hinten"
                        ],
                        "cons": [
                            "Akku fest verbaut (nicht wechselbar)",
                            "Keine Bildkontrolle ohne App"
                        ],
                        "specs": [
                            "Auflösung: 5.3K bei 60 FPS",
                            "Sensor: 1/1.9 Zoll CMOS",
                            "Akku: 1500 mAh integriert",
                            "Gewicht: 133 g"
                        ]
                    }
                ],
                "buying_guide": "### Kaufratgeber Actionkameras: Was ist wirklich wichtig?\n\n#### 1. Sensorgröße und Low-Light-Performance\nEin größerer Sensor (wie 1/1.3 Zoll bei DJI und Insta360) kann mehr Licht einfangen. Dies ist besonders wichtig bei bewölktem Himmel, im Wald oder bei Dämmerung. Günstige oder ältere Modelle schwächeln bei schlechtem Licht stark und erzeugen Bildrauschen.\n\n#### 2. Stabilisierung (Elektronischer Bildstabilisator)\nStabilisierung ist das Herzstück einer Actioncam. GoPros HyperSmooth und DJIs RockSteady eliminieren selbst stärkste Vibrationen beim Mountainbiken oder Skifahren. Auch die 360-Grad-Horizontsperre ist extrem nützlich: Sie hält das Bild waagerecht, selbst wenn die Kamera komplett auf den Kopf gestellt wird.\n\n#### 3. Akkuleistung bei extremen Temperaturen\nKälte ist der Feind von Lithium-Ionen-Akkus. GoPro verbaut spezielle Enduro-Akkus, die auch bei Minustemperaturen im Schnee zuverlässig funktionieren. DJI hat mit der Action 5 Pro die Akkulaufzeit auf Rekordniveau angehoben, sodass die Kamera bis zu 4 Stunden durchhält.",
                "faq": [
                    {
                        "question": "Braucht man eine Schutzhülle zum Tauchen?",
                        "answer": "Die meisten modernen Actionkameras (wie die GoPro Hero 13 oder DJI Osmo Action 5) sind ohne zusätzliches Gehäuse bis zu 10 oder sogar 20 Meter Tiefe wasserdicht. Für tiefere Tauchgänge empfiehlt sich jedoch ein spezielles Schutzgehäuse."
                    },
                    {
                        "question": "Welche Speicherkarte ist notwendig?",
                        "answer": "Sie benötigen eine microSD-Karte mit mindestens U3- oder V30-Klassifizierung, um die extrem hohen Schreibgeschwindigkeiten bei 4K- oder 5.3K-Videoaufnahmen zu gewährleisten."
                    },
                    {
                        "question": "Kann man Actionkameras als Webcam nutzen?",
                        "answer": "Ja, sowohl GoPro als auch DJI bieten offizielle Desktop-Software an, mit der die Kameras per USB-C-Kabel als hochauflösende Webcams für Zoom, Teams oder OBS eingerichtet werden können."
                    },
                    {
                        "question": "Was ist der Vorteil eines klappbaren Displays?",
                        "answer": "Klappbildschirme (wie bei der Insta360 Ace Pro) machen es Vloggern extrem leicht, sich selbst perfekt im Bild zu positionieren, da das Display um 180 Grad nach oben geklappt werden kann."
                    },
                    {
                        "question": "Können externe Mikrofone angeschlossen werden?",
                        "answer": "Ja, über entsprechende USB-C-zu-Klinke-Adapter oder Funkstrecken (wie das DJI Mic oder Rode Wireless GO) lassen sich professionelle externe Mikrofone für perfekten Vlogging-Ton betreiben."
                    }
                ]
            }
        }
    ]

    with app.app_context():
        for post_data in posts_data:
            existing = BlogPost.query.filter_by(slug=post_data["slug"]).first()
            if existing:
                print(f"Deleting existing post: {existing.title}")
                db.session.delete(existing)
                db.session.commit()

            db.session.add(BlogPost(
                title=post_data["title"],
                slug=post_data["slug"],
                excerpt=post_data["excerpt"],
                content_html="",
                category="Gear",
                tags=post_data["tags"],
                cover_image_url=post_data["cover_image_url"],
                status="published",
                published_at=datetime.now(timezone.utc),
                meta_title=post_data["title"],
                meta_description=post_data["excerpt"],
                read_time=8,
                template=post_data["template"],
                structured_content=post_data["structured_content"]
            ))
            print(f"Added post: {post_data['title']}")

        db.session.commit()
        print("Successfully seeded custom posts!")

if __name__ == "__main__":
    seed_custom_posts()
