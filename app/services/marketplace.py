from urllib.parse import quote_plus
def platform_url(platform,query):
    q=quote_plus(query)
    return {"Amazon":f"https://www.amazon.in/s?k={q}","Flipkart":f"https://www.flipkart.com/search?q={q}",
            "IKEA":f"https://www.ikea.com/in/en/search/?q={q}","Swiggy":f"https://www.swiggy.com/search?query={q}",
            "Zomato":f"https://www.zomato.com/search?query={q}","OYO":f"https://www.oyorooms.com/search?location={q}"}.get(platform,f"https://www.google.com/search?q={q}")
HOME_CATALOG=[("LED Ceiling Light","lighting","Amazon",1499),("Ceiling Fan","fan","Amazon",2499),("Compact Dining Table","furniture","IKEA",8990),("Storage Cabinet","storage","IKEA",6990),("Decorative Wall Art","decor","Flipkart",1299),("Bedside Lamp","lighting","IKEA",1999),("Area Rug","decor","Amazon",2499),("Accent Chair","furniture","IKEA",7990)]
PARTY_CATALOG=[("Catering meal package","catering","Swiggy",250),("Party snacks package","catering","Zomato",180),("Simple decoration kit","decoration","Amazon",1999),("Balloon decoration","decoration","Flipkart",2499),("Budget event stay","accommodation","OYO",1800),("Cake delivery","food","Swiggy",900)]
JEWELRY_CATALOG=[("Minimal gold-tone necklace","necklace","Amazon",1499),("Pearl drop earrings","earrings","Flipkart",1199),("Classic bracelet","bracelet","Amazon",999),("Statement earrings","earrings","Flipkart",1799),("Pendant set","set","Amazon",2299)]
