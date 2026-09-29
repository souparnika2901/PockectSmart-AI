from app.services.marketplace import HOME_CATALOG,PARTY_CATALOG,JEWELRY_CATALOG,platform_url

from app.services.gemini_service import generate


def items(catalog):

    return [{"name":n,"category":c,"platform":p,"estimated_price":pr,"currency":"INR","reason":f"Demo option from {p} suitable for the requested budget.","url":platform_url(p,n)} for n,c,p,pr in catalog[:6]]


def fallback_home(r):

    return {"summary":f"A practical {r.style} setup for {', '.join(r.rooms)} within ₹{r.budget:,.0f}.","allocation":{"furniture":r.budget*.45,"lighting":r.budget*.15,"decor":r.budget*.20,"storage":r.budget*.20},"tips":["Prioritize essential furniture first.","Compare dimensions and warranty.","Keep a small reserve for delivery or installation."],"recommendations":items(HOME_CATALOG)}


def fallback_party(r):

    return {"summary":f"A {r.event_type} plan for {r.guests} guests with a ₹{r.budget:,.0f} budget.","allocation":{"catering":r.budget*.45,"decoration":r.budget*.20,"entertainment":r.budget*.15,"venue/accommodation":r.budget*.20},"tips":["Confirm per-person food pricing.","Reserve the venue early.","Keep a contingency amount."],"recommendations":items(PARTY_CATALOG)}


def fallback_jewelry(r):

    return {"summary":f"Jewelry ideas for a {r.occasion} occasion with {r.outfit_style} styling.","allocation":{"necklace":r.budget*.35,"earrings":r.budget*.25,"bracelet":r.budget*.20,"reserve":r.budget*.20},"tips":["Match metal tone with the outfit.","Keep jewelry simpler with detailed outfits.","Verify material, size and return policy."],"recommendations":items(JEWELRY_CATALOG)}


def cat_text(c): return "\n".join(f"- {n} | category={k} | platform={p} | price=INR {v}" for n,k,p,v in c)


def normalize(x,planner,budget,source):

    x["planner"]=planner;x["budget"]=budget;x["source"]=source;x.setdefault("allocation",{});x.setdefault("tips",[]);x.setdefault("recommendations",[]);x.setdefault("summary","Personalized budget recommendations.")

    for i in x["recommendations"]:

        i.setdefault("currency","INR");i.setdefault("estimated_price",0);i.setdefault("reason","Budget-compatible option.");i.setdefault("url",platform_url(i.get("platform","Amazon"),i.get("name","product")))

    x["disclaimer"]="Prices and availability are estimates. Verify on the linked platform before purchase."

    return x


def home(r):

    fb=fallback_home(r); p=f"Planner: Home Interior\nBudget: INR {r.budget}\nRooms: {r.rooms}\nStyle: {r.style}\nNotes: {r.notes}\nCatalog:\n{cat_text(HOME_CATALOG)}\nReturn a sensible allocation and 4-6 catalog recommendations without exceeding the total budget."

    try:
        x,s=generate(p); return normalize(x,"home",r.budget,s)

    except Exception as e:

        print("GEMINI ERROR:", repr(e))

        return normalize(fb,"home",r.budget,"fallback")


def party(r):

    fb=fallback_party(r); p=f"Planner: Party\nBudget: INR {r.budget}\nGuests: {r.guests}\nEvent: {r.event_type}\nVenue: {r.venue}\nCity: {r.city}\nNotes: {r.notes}\nCatalog:\n{cat_text(PARTY_CATALOG)}\nAllocate sensibly and do not claim live availability."

    try:
        x,s=generate(p); return normalize(x,"party",r.budget,s)

    except Exception as e:

        print("GEMINI ERROR:", repr(e))

        return normalize(fb,"party",r.budget,"fallback")


def jewelry(r,image_bytes=None,mime_type=None):

    fb=fallback_jewelry(r); p=f"Planner: Jewelry\nBudget: INR {r.budget}\nOccasion: {r.occasion}\nOutfit style: {r.outfit_style}\nMetal: {r.metal}\nNotes: {r.notes}\nCatalog:\n{cat_text(JEWELRY_CATALOG)}\nIf an outfit image is supplied, use only visible style, colour and formality. Do not infer sensitive personal attributes."

    try:
        x,s=generate(p,image_bytes,mime_type); return normalize(x,"jewelry",r.budget,s)

    except Exception as e:

        print("GEMINI ERROR:", repr(e))

        return normalize(fb,"jewelry",r.budget,"fallback")