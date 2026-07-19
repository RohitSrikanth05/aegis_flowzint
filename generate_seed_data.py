import json
import os


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def availability(stock: int) -> str:

    if stock == 0:
        return "Out of Stock"

    if stock <= 10:
        return "Limited Stock"

    return "In Stock"


def build_product_content(product, category):
    return f"""Product Name: {product["title"]}
Brand: {product["brand"]}
Series: {product["series"]}
Model: {product["model"]}
Category: {category.title()}
Description: {product["description"]}
Price: ₹{product["price"]:,}
Rating: {product["rating"]}/5 ({product["review_count"]} verified reviews)
Availability: {availability(product["stock"])}
Warranty: {product["warranty"]}
Launch Year: {product["release_year"]}
Available Colours: {", ".join(product["colors"])}
Key Specifications: {", ".join(product["specifications"])}
Recommended For: {", ".join(product["recommended_for"])}
Search Keywords: {", ".join(product["keywords"])}""".strip()


# ==========================================================
# PRODUCT CATALOG
# ==========================================================

product_catalog = {

    # ======================================================
    # AUDIO
    # ======================================================

    "audio": [

        {
            "title": "NovaBuds Lite",
            "brand": "Nova",
            "series": "NovaBuds",
            "model": "Lite",
            "price": 2999,
            "rating": 4.4,
            "review_count": 1842,
            "stock": 56,
            "release_year": 2025,
            "warranty": "1 Year",
            "colors": ["Black", "White", "Blue"],
            "description": "Affordable true wireless earbuds offering balanced sound, long battery life and reliable everyday performance.",
            "specifications": ["10 mm Dynamic Drivers", "Bluetooth 5.4", "30-hour Battery", "USB-C Fast Charging", "IPX5 Water Resistance"],
            "recommended_for": ["Students", "Music", "Daily Commute"],
            "keywords": ["earbuds", "tws", "budget", "bluetooth", "wireless audio"]
        },

        {
            "title": "NovaBuds Pro",
            "brand": "Nova",
            "series": "NovaBuds",
            "model": "Pro",
            "price": 7999,
            "rating": 4.8,
            "review_count": 6148,
            "stock": 37,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Silver", "Purple"],
            "description": "Premium wireless earbuds with adaptive active noise cancellation and immersive high-resolution audio.",
            "specifications": ["Adaptive ANC", "Hi-Res Audio", "Wireless Charging", "Bluetooth 5.4", "40-hour Battery"],
            "recommended_for": ["Professionals", "Travel", "Music Enthusiasts"],
            "keywords": ["premium earbuds", "anc", "noise cancellation", "hi-res audio", "wireless"]
        },

        {
            "title": "NovaSound Mini",
            "brand": "Nova",
            "series": "NovaSound",
            "model": "Mini",
            "price": 3499,
            "rating": 4.5,
            "review_count": 2187,
            "stock": 42,
            "release_year": 2025,
            "warranty": "1 Year",
            "colors": ["Black", "Blue", "Red"],
            "description": "Compact Bluetooth speaker designed for portable entertainment with surprisingly powerful sound.",
            "specifications": ["20W Output", "Bluetooth 5.3", "IPX7 Waterproof", "15-hour Battery", "USB-C Charging"],
            "recommended_for": ["Travel", "Outdoor", "Casual Listening"],
            "keywords": ["speaker", "portable", "bluetooth speaker", "waterproof", "travel"]
        },

        {
            "title": "NovaSound Max",
            "brand": "Nova",
            "series": "NovaSound",
            "model": "Max",
            "price": 8999,
            "rating": 4.8,
            "review_count": 4021,
            "stock": 25,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Grey"],
            "description": "Large portable Bluetooth speaker delivering room-filling sound with deep bass and extended battery life.",
            "specifications": ["80W Output", "Bluetooth 5.4", "24-hour Battery", "Stereo Pairing", "IP67 Protection"],
            "recommended_for": ["Parties", "Outdoor Events", "Entertainment"],
            "keywords": ["party speaker", "bass", "portable speaker", "wireless", "bluetooth"]
        },

        {
            "title": "Nova ANC Headphones",
            "brand": "Nova",
            "series": "NovaHead",
            "model": "ANC",
            "price": 11999,
            "rating": 4.7,
            "review_count": 3561,
            "stock": 29,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Silver"],
            "description": "Over-ear wireless headphones featuring adaptive ANC and studio-inspired sound tuning.",
            "specifications": ["Adaptive ANC", "50-hour Battery", "Hi-Res Audio", "USB-C", "Multipoint Pairing"],
            "recommended_for": ["Work", "Travel", "Music"],
            "keywords": ["headphones", "anc", "wireless", "travel", "office"]
        },

        {
            "title": "Nova Studio Headphones",
            "brand": "Nova",
            "series": "NovaHead",
            "model": "Studio",
            "price": 14999,
            "rating": 4.9,
            "review_count": 1863,
            "stock": 18,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Black"],
            "description": "Professional wired monitoring headphones built for audio production and accurate sound reproduction.",
            "specifications": ["Studio Drivers", "Detachable Cable", "High Impedance", "Closed Back", "Memory Foam Cushions"],
            "recommended_for": ["Music Production", "Editing", "Content Creation"],
            "keywords": ["studio headphones", "music production", "editing", "monitoring", "professional"]
        },

        {
            "title": "Nova Speaker X",
            "brand": "Nova",
            "series": "NovaSound",
            "model": "X",
            "price": 15999,
            "rating": 4.9,
            "review_count": 2921,
            "stock": 17,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "White"],
            "description": "Premium smart home speaker combining high-fidelity audio with integrated voice assistant support.",
            "specifications": ["120W Audio", "Wi-Fi", "Bluetooth", "Smart Assistant", "Multi-room Audio"],
            "recommended_for": ["Home", "Smart Living", "Entertainment"],
            "keywords": ["smart speaker", "wifi speaker", "home audio", "assistant", "premium"]
        },

        {
            "title": "Nova Party Box",
            "brand": "Nova",
            "series": "NovaSound",
            "model": "Party Box",
            "price": 24999,
            "rating": 4.8,
            "review_count": 1548,
            "stock": 11,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black"],
            "description": "High-power party speaker with dynamic lighting, karaoke support and massive sound output.",
            "specifications": ["160W Output", "RGB Lighting", "Microphone Input", "Bluetooth 5.4", "18-hour Battery"],
            "recommended_for": ["Parties", "Events", "Outdoor Entertainment"],
            "keywords": ["party", "karaoke", "speaker", "events", "bluetooth"]
        }

    ],

    # ======================================================
    # LAPTOPS
    # ======================================================

    "laptop": [

        {
            "title": "NovaBook Student",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Student",
            "price": 44999,
            "rating": 4.5,
            "review_count": 3214,
            "stock": 43,
            "release_year": 2025,
            "warranty": "2 Years",
            "colors": ["Silver", "Blue"],
            "description": "Affordable laptop built for students, online learning, programming and everyday productivity.",
            "specifications": ["Intel Core i3-1315U", "8GB DDR5 RAM", "512GB NVMe SSD", "14-inch Full HD IPS Display", "Wi-Fi 6", "Backlit Keyboard", "9-hour Battery"],
            "recommended_for": ["Students", "Programming", "Office Work"],
            "keywords": ["budget laptop", "student laptop", "college", "coding", "office"]
        },

        {
            "title": "NovaBook Air",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Air",
            "price": 64999,
            "rating": 4.7,
            "review_count": 4172,
            "stock": 34,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Silver", "Space Grey", "Blue"],
            "description": "Thin and lightweight ultrabook designed for portability, long battery life and premium everyday computing.",
            "specifications": ["Intel Core Ultra 5", "16GB LPDDR5 RAM", "512GB PCIe Gen4 SSD", "14-inch 2.8K IPS Display", "Thunderbolt 4", "Fingerprint Reader", "16-hour Battery"],
            "recommended_for": ["Professionals", "Students", "Travel"],
            "keywords": ["ultrabook", "lightweight laptop", "portable", "office", "battery life"]
        },

        {
            "title": "NovaBook Business",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Business",
            "price": 79999,
            "rating": 4.8,
            "review_count": 2891,
            "stock": 22,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Black", "Silver"],
            "description": "Professional business laptop featuring enterprise-grade security, reliability and all-day productivity.",
            "specifications": ["Intel Core Ultra 7", "16GB DDR5 RAM", "1TB NVMe SSD", "14-inch IPS Display", "Windows 11 Pro", "Fingerprint Reader", "IR Face Unlock"],
            "recommended_for": ["Business", "Corporate", "Office"],
            "keywords": ["business laptop", "office", "enterprise", "security", "windows pro"]
        },

        {
            "title": "NovaBook Creator",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Creator",
            "price": 114999,
            "rating": 4.8,
            "review_count": 2174,
            "stock": 18,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Graphite", "Silver"],
            "description": "Creator-focused laptop engineered for professional photo editing, 4K video production, animation and graphic design workflows.",
            "specifications": ["AMD Ryzen AI 9 Processor", "NVIDIA RTX 4060 8GB", "32GB DDR5 RAM", "1TB PCIe Gen4 SSD", "15.6-inch 3K OLED Display", "100% DCI-P3 Colour Gamut", "SD Card Reader"],
            "recommended_for": ["Video Editing", "Photography", "Graphic Design"],
            "keywords": ["creator laptop", "video editing", "photoshop", "premiere pro", "davinci resolve", "oled", "rtx"]
        },

        {
            "title": "NovaBook Gaming",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Gaming",
            "price": 139999,
            "rating": 4.9,
            "review_count": 5128,
            "stock": 14,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Matte Black"],
            "description": "Flagship gaming laptop delivering desktop-class performance for AAA gaming, streaming, AI development and demanding creative workloads.",
            "specifications": ["Intel Core Ultra 9 285H", "NVIDIA RTX 5070 Laptop GPU 12GB", "32GB DDR5-6400 RAM", "2TB PCIe Gen4 SSD", "16-inch QHD+ 240Hz IPS Display", "Per-Key RGB Keyboard", "Wi-Fi 7"],
            "recommended_for": ["Gaming", "Streaming", "Machine Learning"],
            "keywords": ["gaming laptop", "rtx 5070", "cuda", "deep learning", "ai", "streaming", "240hz"]
        },

        {
            "title": "NovaBook AI",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "AI",
            "price": 124999,
            "rating": 4.9,
            "review_count": 1846,
            "stock": 17,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Silver", "Midnight Blue"],
            "description": "AI-first laptop designed for local inference, LLM experimentation, software development and next-generation productivity applications.",
            "specifications": ["AMD Ryzen AI 9 HX Processor", "Dedicated 50+ TOPS NPU", "32GB LPDDR5X RAM", "2TB PCIe Gen4 SSD", "16-inch 2.8K OLED Display", "Wi-Fi 7", "Thunderbolt 4"],
            "recommended_for": ["Artificial Intelligence", "Software Development", "Data Science"],
            "keywords": ["ai laptop", "llm", "machine learning", "python", "programming", "npu", "local inference"]
        },

        {
            "title": "NovaBook Ultra",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Ultra",
            "price": 159999,
            "rating": 4.9,
            "review_count": 1628,
            "stock": 9,
            "release_year": 2026,
            "warranty": "4 Years",
            "colors": ["Titanium Grey", "Midnight Black"],
            "description": "Premium flagship ultrabook combining exceptional portability with workstation-level performance for executives and power users.",
            "specifications": ["Intel Core Ultra 9", "32GB LPDDR5X RAM", "2TB PCIe Gen5 SSD", "16-inch 3.2K OLED Touch Display", "Thunderbolt 5", "Wi-Fi 7", "18-hour Battery"],
            "recommended_for": ["Executives", "Professionals", "Power Users"],
            "keywords": ["flagship laptop", "premium ultrabook", "oled", "business", "portable", "high performance"]
        },

        {
            "title": "NovaBook Workstation",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Workstation",
            "price": 219999,
            "rating": 4.9,
            "review_count": 937,
            "stock": 6,
            "release_year": 2026,
            "warranty": "5 Years",
            "colors": ["Matte Black"],
            "description": "Professional mobile workstation engineered for CAD, simulation, AI research, engineering and 3D rendering.",
            "specifications": ["Intel Xeon-class Processor", "NVIDIA RTX 5000 Ada Professional GPU", "64GB ECC DDR5 RAM", "4TB PCIe Gen5 SSD", "17-inch 4K Mini-LED Display", "ISV Certified", "Dual Thunderbolt 5"],
            "recommended_for": ["Engineering", "Architecture", "3D Rendering"],
            "keywords": ["workstation", "cad", "solidworks", "autocad", "blender", "rendering", "engineering"]
        },

        {
            "title": "NovaBook Enterprise",
            "brand": "Nova",
            "series": "NovaBook",
            "model": "Enterprise",
            "price": 99999,
            "rating": 4.8,
            "review_count": 1406,
            "stock": 19,
            "release_year": 2026,
            "warranty": "4 Years On-site",
            "colors": ["Black", "Silver"],
            "description": "Enterprise-ready laptop focused on security, remote management, long-term reliability and corporate deployment.",
            "specifications": ["Intel Core Ultra 7", "32GB DDR5 RAM", "1TB PCIe Gen4 SSD", "Windows 11 Pro", "TPM 2.0", "Smart Card Reader", "vPro Enterprise"],
            "recommended_for": ["Corporate IT", "Finance", "Government"],
            "keywords": ["enterprise", "corporate", "security", "vpro", "windows pro", "business laptop"]
        }

    ],

    # ======================================================
    # MOBILE PHONES
    # ======================================================

    "mobile": [

        {
            "title": "NovaPhone Lite",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Lite",
            "price": 14999,
            "rating": 4.4,
            "review_count": 7842,
            "stock": 73,
            "release_year": 2025,
            "warranty": "1 Year",
            "colors": ["Black", "Blue", "Mint"],
            "description": "Affordable smartphone delivering dependable performance, long battery life and an excellent everyday user experience.",
            "specifications": ["6.6-inch FHD+ LCD", "5000mAh Battery", "50MP AI Camera", "6GB RAM", "128GB Storage", "33W Fast Charging"],
            "recommended_for": ["Students", "Daily Use", "First Smartphone"],
            "keywords": ["budget phone", "android", "student", "battery", "value"]
        },

        {
            "title": "NovaPhone Neo",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Neo",
            "price": 24999,
            "rating": 4.6,
            "review_count": 5936,
            "stock": 48,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Blue", "Silver"],
            "description": "Balanced mid-range smartphone combining excellent cameras, smooth performance and all-day battery life.",
            "specifications": ["6.7-inch AMOLED 120Hz", "5500mAh Battery", "8GB RAM", "256GB Storage", "67W Fast Charging", "50MP OIS Camera"],
            "recommended_for": ["Photography", "Entertainment", "Everyday Users"],
            "keywords": ["midrange phone", "amoled", "camera", "android", "120hz"]
        },

        {
            "title": "NovaPhone Edge",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Edge",
            "price": 39999,
            "rating": 4.8,
            "review_count": 4381,
            "stock": 35,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Graphite", "Titanium", "Blue"],
            "description": "Camera-first flagship smartphone designed for photography enthusiasts with professional imaging features.",
            "specifications": ["6.78-inch AMOLED 120Hz Display", "50MP Sony Main Sensor with OIS", "50MP Ultra-Wide Camera", "32MP Selfie Camera", "12GB RAM", "256GB Storage", "80W Fast Charging"],
            "recommended_for": ["Photography", "Content Creation", "Travel"],
            "keywords": ["camera phone", "photography", "flagship", "android", "ois", "creator"]
        },

        {
            "title": "NovaPhone Max",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Max",
            "price": 34999,
            "rating": 4.7,
            "review_count": 5126,
            "stock": 41,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Blue", "Green"],
            "description": "Battery-focused smartphone engineered for power users requiring exceptional endurance and dependable performance.",
            "specifications": ["6500mAh Battery", "67W Fast Charging", "6.8-inch AMOLED Display", "8GB RAM", "256GB Storage", "Stereo Speakers", "IP68 Water Resistance"],
            "recommended_for": ["Business", "Travel", "Heavy Users"],
            "keywords": ["battery phone", "long battery", "travel", "business", "power user"]
        },

        {
            "title": "NovaPhone Gaming",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Gaming",
            "price": 49999,
            "rating": 4.9,
            "review_count": 3652,
            "stock": 22,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Matte Black"],
            "description": "Gaming smartphone optimized for competitive mobile gaming with flagship performance and advanced cooling.",
            "specifications": ["Snapdragon Elite-class Processor", "16GB LPDDR5X RAM", "512GB UFS 4.1 Storage", "6.8-inch AMOLED 165Hz Display", "6000mAh Battery", "120W Fast Charging", "Vapor Chamber Cooling"],
            "recommended_for": ["Gaming", "Streaming", "Esports"],
            "keywords": ["gaming phone", "165hz", "snapdragon", "esports", "high performance", "streaming"]
        },

        {
            "title": "NovaPhone Ultra",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Ultra",
            "price": 79999,
            "rating": 4.9,
            "review_count": 2978,
            "stock": 16,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Titanium Black", "Titanium Silver"],
            "description": "Ultimate flagship smartphone delivering top-tier cameras, display technology and AI-powered productivity features.",
            "specifications": ["6.9-inch LTPO AMOLED 144Hz", "Snapdragon Elite-class Processor", "16GB LPDDR5X RAM", "512GB UFS 4.1 Storage", "200MP Main Camera", "100W Wired Charging", "50W Wireless Charging"],
            "recommended_for": ["Professionals", "Photography", "Power Users"],
            "keywords": ["ultra flagship", "200mp", "premium phone", "wireless charging", "ai", "camera"]
        },

        {
            "title": "NovaPhone Fold",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Fold",
            "price": 129999,
            "rating": 4.8,
            "review_count": 1743,
            "stock": 11,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Titanium Black", "Silver"],
            "description": "Premium foldable smartphone designed for multitasking, productivity and immersive entertainment.",
            "specifications": ["7.8-inch Foldable LTPO AMOLED", "6.3-inch Cover Display", "Snapdragon Elite-class Processor", "16GB LPDDR5X RAM", "512GB Storage", "Triple 50MP Camera System", "Wireless Charging"],
            "recommended_for": ["Business", "Productivity", "Multitasking"],
            "keywords": ["foldable", "productivity", "business", "multitasking", "premium"]
        },

        {
            "title": "NovaPhone Compact",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Compact",
            "price": 54999,
            "rating": 4.8,
            "review_count": 2834,
            "stock": 27,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Silver", "Green"],
            "description": "Compact flagship smartphone offering premium performance in a comfortable one-handed design.",
            "specifications": ["6.1-inch LTPO AMOLED", "Snapdragon Elite-class Processor", "12GB LPDDR5X RAM", "256GB Storage", "50MP OIS Camera", "Wireless Charging"],
            "recommended_for": ["Travel", "Photography", "Everyday Use"],
            "keywords": ["compact phone", "small flagship", "travel", "camera", "premium"]
        },

        {
            "title": "NovaPhone Business",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Business",
            "price": 59999,
            "rating": 4.7,
            "review_count": 1987,
            "stock": 21,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Black", "Grey"],
            "description": "Business-oriented smartphone focused on enterprise security, productivity and reliable communication.",
            "specifications": ["6.7-inch AMOLED Display", "Enterprise Security Suite", "12GB RAM", "256GB Storage", "6000mAh Battery", "Wi-Fi 7"],
            "recommended_for": ["Business", "Corporate", "Productivity"],
            "keywords": ["business phone", "enterprise", "security", "office", "productivity"]
        },

        {
            "title": "NovaPhone Explorer",
            "brand": "Nova",
            "series": "NovaPhone",
            "model": "Explorer",
            "price": 45999,
            "rating": 4.7,
            "review_count": 1462,
            "stock": 18,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Black", "Orange"],
            "description": "Rugged smartphone engineered for outdoor adventures, field work and harsh environments.",
            "specifications": ["MIL-STD-810H Certified", "IP69 Rating", "6500mAh Battery", "8GB RAM", "256GB Storage", "Satellite SOS Support"],
            "recommended_for": ["Adventure", "Construction", "Field Work"],
            "keywords": ["rugged phone", "outdoor", "waterproof", "ip69", "durable"]
        }

    ],

    # ======================================================
    # WEARABLES
    # ======================================================

    "wearables": [

        {
            "title": "NovaFit Band",
            "brand": "Nova",
            "series": "NovaFit",
            "model": "Band",
            "price": 2499,
            "rating": 4.5,
            "review_count": 9184,
            "stock": 74,
            "release_year": 2025,
            "warranty": "1 Year",
            "colors": ["Black", "Blue", "Pink"],
            "description": "Lightweight fitness band offering all-day activity tracking, sleep monitoring and excellent battery life.",
            "specifications": ["AMOLED Display", "Heart Rate Sensor", "SpO2 Monitoring", "Sleep Tracking", "10-Day Battery"],
            "recommended_for": ["Fitness", "Walking", "Students"],
            "keywords": ["fitness band", "health", "sleep", "step tracker", "budget wearable"]
        },

        {
            "title": "NovaWatch Lite",
            "brand": "Nova",
            "series": "NovaWatch",
            "model": "Lite",
            "price": 5999,
            "rating": 4.6,
            "review_count": 4837,
            "stock": 53,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Silver", "Blue"],
            "description": "Affordable smartwatch combining fitness tracking, Bluetooth calling and smart notifications.",
            "specifications": ["1.8-inch AMOLED", "Bluetooth Calling", "GPS", "SpO2", "7-Day Battery"],
            "recommended_for": ["Daily Wear", "Fitness", "Students"],
            "keywords": ["smartwatch", "bluetooth calling", "fitness", "gps", "wearable"]
        },

        {
            "title": "NovaWatch Pro",
            "brand": "Nova",
            "series": "NovaWatch",
            "model": "Pro",
            "price": 11999,
            "rating": 4.8,
            "review_count": 3714,
            "stock": 34,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Silver", "Titanium"],
            "description": "Premium smartwatch offering advanced health monitoring, GPS navigation and productivity features.",
            "specifications": ["1.92-inch AMOLED", "Dual-Band GPS", "ECG", "Blood Oxygen Sensor", "Stress Monitoring", "Wireless Charging", "10-Day Battery"],
            "recommended_for": ["Professionals", "Fitness", "Health Monitoring"],
            "keywords": ["premium smartwatch", "ecg", "gps", "health", "wearable"]
        },

        {
            "title": "NovaWatch Ultra",
            "brand": "Nova",
            "series": "NovaWatch",
            "model": "Ultra",
            "price": 24999,
            "rating": 4.9,
            "review_count": 2198,
            "stock": 19,
            "release_year": 2026,
            "warranty": "3 Years",
            "colors": ["Titanium Grey", "Titanium Black"],
            "description": "Flagship adventure smartwatch engineered for extreme sports, hiking and endurance athletes.",
            "specifications": ["Titanium Body", "Military Grade Durability", "Dual-Band GPS", "LTE Connectivity", "14-Day Battery", "Offline Maps", "Depth Sensor"],
            "recommended_for": ["Adventure", "Hiking", "Triathlon"],
            "keywords": ["adventure watch", "gps", "outdoor", "sports", "ultra"]
        },

        {
            "title": "Nova Health Tracker",
            "brand": "Nova",
            "series": "NovaHealth",
            "model": "Tracker",
            "price": 7999,
            "rating": 4.7,
            "review_count": 2864,
            "stock": 41,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Blue"],
            "description": "Dedicated health wearable focused on continuous wellness monitoring and preventive healthcare insights.",
            "specifications": ["ECG", "HRV Analysis", "Blood Oxygen", "Stress Detection", "Sleep Analysis", "7-Day Battery"],
            "recommended_for": ["Healthcare", "Wellness", "Senior Citizens"],
            "keywords": ["health tracker", "ecg", "heart rate", "wellness", "sleep"]
        },

        {
            "title": "Nova Sport Watch",
            "brand": "Nova",
            "series": "NovaSport",
            "model": "Sport",
            "price": 9999,
            "rating": 4.8,
            "review_count": 2675,
            "stock": 37,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "Orange", "Blue"],
            "description": "Sports smartwatch designed for runners, cyclists and endurance athletes requiring detailed performance metrics.",
            "specifications": ["VO2 Max Tracking", "Dual GPS", "Training Analytics", "Heart Rate", "Water Resistance 5ATM", "10-Day Battery"],
            "recommended_for": ["Running", "Cycling", "Sports"],
            "keywords": ["sports watch", "running", "cycling", "training", "gps"]
        },

        {
            "title": "Nova Ring",
            "brand": "Nova",
            "series": "NovaRing",
            "model": "Smart Ring",
            "price": 18999,
            "rating": 4.7,
            "review_count": 1387,
            "stock": 15,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Silver", "Black", "Gold"],
            "description": "Premium smart ring delivering continuous health tracking and sleep analysis in a compact form factor.",
            "specifications": ["Heart Rate", "Sleep Tracking", "HRV Monitoring", "Temperature Sensor", "7-Day Battery"],
            "recommended_for": ["Health", "Sleep", "Minimalists"],
            "keywords": ["smart ring", "sleep", "wellness", "health", "ring wearable"]
        },

        {
            "title": "Nova Kids Watch",
            "brand": "Nova",
            "series": "NovaWatch",
            "model": "Kids",
            "price": 4999,
            "rating": 4.5,
            "review_count": 2043,
            "stock": 58,
            "release_year": 2025,
            "warranty": "1 Year",
            "colors": ["Blue", "Pink", "Green"],
            "description": "GPS-enabled smartwatch built for children's safety with communication and parental control features.",
            "specifications": ["GPS Tracking", "SOS Button", "Video Calling", "Parental Controls", "IP68 Water Resistance"],
            "recommended_for": ["Children", "School", "Family"],
            "keywords": ["kids watch", "gps", "safety", "parents", "children"]
        }

    ],

    # ======================================================
    # ACCESSORIES
    # ======================================================

    "accessories": [

        {
            "title": "Nova Mechanical Keyboard",
            "brand": "Nova",
            "series": "NovaKeys",
            "model": "Mechanical Pro",
            "price": 6499,
            "rating": 4.8,
            "review_count": 5136,
            "stock": 48,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "White"],
            "description": "Premium mechanical keyboard featuring hot-swappable switches, per-key RGB lighting and an aluminium chassis.",
            "specifications": ["Hot-swappable Switches", "Per-Key RGB", "USB-C", "N-Key Rollover", "Aluminium Frame", "Detachable Cable"],
            "recommended_for": ["Programming", "Gaming", "Office"],
            "keywords": ["mechanical keyboard", "rgb", "gaming", "typing", "programming"]
        },

        {
            "title": "Nova Gaming Mouse",
            "brand": "Nova",
            "series": "NovaAim",
            "model": "Elite",
            "price": 2999,
            "rating": 4.7,
            "review_count": 7348,
            "stock": 76,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black", "White"],
            "description": "Ultra-light gaming mouse designed for competitive gaming with exceptional tracking accuracy.",
            "specifications": ["26000 DPI Optical Sensor", "Ultra-Lightweight Design", "8 Programmable Buttons", "RGB Lighting", "1000Hz Polling Rate"],
            "recommended_for": ["Gaming", "Esports", "Design"],
            "keywords": ["gaming mouse", "rgb", "esports", "high dpi", "lightweight"]
        },

        {
            "title": "Nova Webcam Pro",
            "brand": "Nova",
            "series": "NovaVision",
            "model": "Pro",
            "price": 5499,
            "rating": 4.6,
            "review_count": 2849,
            "stock": 42,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black"],
            "description": "Professional webcam delivering crystal-clear 4K video for meetings, streaming and online teaching.",
            "specifications": ["4K Resolution", "HDR", "Auto Focus", "Dual Noise-Cancelling Microphones", "USB Plug-and-Play"],
            "recommended_for": ["Meetings", "Streaming", "Teaching"],
            "keywords": ["webcam", "4k", "streaming", "zoom", "online meetings"]
        },

        {
            "title": "Nova USB-C Dock",
            "brand": "Nova",
            "series": "NovaDock",
            "model": "11-in-1",
            "price": 7999,
            "rating": 4.7,
            "review_count": 1968,
            "stock": 34,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Space Grey"],
            "description": "Professional USB-C docking station expanding laptops into full desktop workstations.",
            "specifications": ["HDMI", "DisplayPort", "Gigabit Ethernet", "SD Card Reader", "100W Power Delivery", "3 USB-A Ports", "USB-C Data Port"],
            "recommended_for": ["Office", "Professionals", "Developers"],
            "keywords": ["usb dock", "usb-c hub", "docking station", "office", "display"]
        },

        {
            "title": "Nova SSD 1TB",
            "brand": "Nova",
            "series": "NovaStorage",
            "model": "Gen4 1TB",
            "price": 8999,
            "rating": 4.9,
            "review_count": 4317,
            "stock": 52,
            "release_year": 2026,
            "warranty": "5 Years",
            "colors": ["Black"],
            "description": "High-speed PCIe Gen4 NVMe SSD designed for gaming, content creation and professional workloads.",
            "specifications": ["1TB Capacity", "7000 MB/s Read", "6500 MB/s Write", "PCIe Gen4 x4", "M.2 2280", "5-Year Warranty"],
            "recommended_for": ["Gaming", "Editing", "Storage Upgrade"],
            "keywords": ["ssd", "nvme", "pcie gen4", "gaming", "storage"]
        },

        {
            "title": "Nova SSD 2TB Pro",
            "brand": "Nova",
            "series": "NovaStorage",
            "model": "Pro 2TB",
            "price": 16999,
            "rating": 4.9,
            "review_count": 2684,
            "stock": 31,
            "release_year": 2026,
            "warranty": "5 Years",
            "colors": ["Black"],
            "description": "Professional NVMe SSD engineered for AI datasets, 4K editing and enterprise storage performance.",
            "specifications": ["2TB Capacity", "7400 MB/s Read", "7000 MB/s Write", "PCIe Gen4", "DRAM Cache", "Hardware Encryption"],
            "recommended_for": ["AI", "Video Editing", "Professional Workstations"],
            "keywords": ["ssd", "2tb", "nvme", "professional", "fast storage"]
        },

        {
            "title": "Nova GaN Charger 100W",
            "brand": "Nova",
            "series": "NovaCharge",
            "model": "GaN 100",
            "price": 3999,
            "rating": 4.8,
            "review_count": 5874,
            "stock": 87,
            "release_year": 2026,
            "warranty": "18 Months",
            "colors": ["White", "Black"],
            "description": "Compact Gallium Nitride fast charger supporting laptops, tablets and smartphones.",
            "specifications": ["100W USB-C PD", "Dual USB-C", "USB-A", "GaN Technology", "Universal Voltage"],
            "recommended_for": ["Travel", "Professionals", "Students"],
            "keywords": ["gan charger", "usb-c", "100w", "fast charging", "travel"]
        },

        {
            "title": "Nova PowerBank 30000",
            "brand": "Nova",
            "series": "NovaPower",
            "model": "30000",
            "price": 4999,
            "rating": 4.8,
            "review_count": 6423,
            "stock": 65,
            "release_year": 2026,
            "warranty": "18 Months",
            "colors": ["Black"],
            "description": "High-capacity power bank capable of charging laptops, tablets and smartphones multiple times.",
            "specifications": ["30000mAh", "65W Power Delivery", "USB-C", "Dual USB-A", "LED Battery Display"],
            "recommended_for": ["Travel", "Business", "Outdoor"],
            "keywords": ["powerbank", "portable charger", "usb-c pd", "travel", "battery"]
        },

        {
            "title": "Nova Laptop Cooling Pad",
            "brand": "Nova",
            "series": "NovaCool",
            "model": "X5",
            "price": 2499,
            "rating": 4.5,
            "review_count": 3251,
            "stock": 58,
            "release_year": 2025,
            "warranty": "1 Year",
            "colors": ["Black"],
            "description": "Laptop cooling pad reducing temperatures during gaming and intensive workloads.",
            "specifications": ["5 Cooling Fans", "RGB Lighting", "Adjustable Height", "USB Powered", "Supports 17-inch Laptops"],
            "recommended_for": ["Gaming", "Engineering", "Editing"],
            "keywords": ["cooling pad", "laptop cooling", "gaming", "thermal"]
        },

        {
            "title": "Nova Ergonomic Laptop Stand",
            "brand": "Nova",
            "series": "NovaDesk",
            "model": "Lift",
            "price": 1999,
            "rating": 4.7,
            "review_count": 4028,
            "stock": 61,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Silver", "Black"],
            "description": "Adjustable aluminium laptop stand improving posture, airflow and workspace ergonomics.",
            "specifications": ["Aluminium Alloy", "Foldable", "Height Adjustable", "Anti-Slip Pads", "Supports up to 17-inch Laptops"],
            "recommended_for": ["Office", "Students", "Developers"],
            "keywords": ["laptop stand", "ergonomic", "desk setup", "office", "productivity"]
        },

        {
            "title": "Nova Wireless Presenter",
            "brand": "Nova",
            "series": "NovaPresent",
            "model": "Pro",
            "price": 3499,
            "rating": 4.6,
            "review_count": 1482,
            "stock": 37,
            "release_year": 2026,
            "warranty": "2 Years",
            "colors": ["Black"],
            "description": "Wireless presentation remote with laser pointer and long-range connectivity for professional presentations.",
            "specifications": ["50m Wireless Range", "Red Laser Pointer", "USB Receiver", "Plug-and-Play", "Rechargeable Battery"],
            "recommended_for": ["Teachers", "Business", "Presentations"],
            "keywords": ["presenter", "laser pointer", "office", "presentation", "wireless"]
        }

    ]

}


# ==========================================================
# FAQ TITLES
# ==========================================================

faqs = [
    "How do I track my order?",
    "Can I cancel an order?",
    "How do refunds work?",
    "Do products come with warranty?",
    "Can I return opened products?",
    "What payment methods are accepted?",
    "How long does shipping take?",
    "Do you ship across India?",
    "Can I exchange a product?",
    "What if I receive a damaged item?",
    "What if I receive the wrong item?",
    "Can I pay via EMI?",
    "Do you offer cash on delivery?",
    "How do I contact support?",
    "Can I update my delivery address?",
    "When will my refund arrive?",
    "Can I preorder products?",
    "Do you sell refurbished devices?",
    "How does express shipping work?",
    "Do accessories have warranty?",
    "Can businesses place bulk orders?",
    "How are returns inspected?",
    "What happens if delivery fails?",
    "Can I schedule delivery?",
    "How do I download invoices?",
    "Do you sell TVs or home appliances?",
    "Do you sell gaming chairs or desks?",
    "Do you sell cameras or DSLRs?",
    "Do you sell printers or scanners?"
]


# ==========================================================
# POLICY TITLES
# ==========================================================

policies = [
    "Refund Policy",
    "Return Policy",
    "Shipping Policy",
    "Warranty Policy",
    "Cancellation Policy",
    "Exchange Policy",
    "COD Policy",
    "EMI Policy",
    "Privacy Policy",
    "Bulk Orders Policy"
]


# ==========================================================
# GENERATION
# ==========================================================

def generate_dataset() -> list:

    data = []

    # Products
    for category, products in product_catalog.items():
        for i, product in enumerate(products, start=1):
            data.append({
                "id": f"{category}_p{i}",
                "type": "product",
                "category": category,
                "title": product["title"],
                "content": build_product_content(product, category),
                "price": product["price"],
                "stock": product["stock"],
                "rating": product["rating"]
            })

    # FAQ stubs — content filled by improve_dataset.py
    for i, faq in enumerate(faqs, start=1):
        data.append({
            "id": f"faq_{i}",
            "type": "faq",
            "category": "support",
            "title": faq,
            "content": f"ShopNova support information regarding: {faq}"
        })

    # Policy stubs — content filled by improve_dataset.py
    for i, policy in enumerate(policies, start=1):
        data.append({
            "id": f"policy_{i}",
            "type": "policy",
            "category": "policy",
            "title": policy,
            "content": f"Official ShopNova {policy.lower()}."
        })

    return data


if __name__ == "__main__":

    output_path = "data/shopnova_data.json"
    os.makedirs("data", exist_ok=True)

    data = generate_dataset()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    products = [i for i in data if i["type"] == "product"]
    faqs_out = [i for i in data if i["type"] == "faq"]
    policies_out = [i for i in data if i["type"] == "policy"]

    print(f"Dataset generated: {len(data)} total documents")
    print(f"  Products : {len(products)}")
    print(f"  FAQs     : {len(faqs_out)}")
    print(f"  Policies : {len(policies_out)}")
    print(f"  Output   : {output_path}")