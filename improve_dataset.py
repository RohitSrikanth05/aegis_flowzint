import json
import os

# ==========================================================
# FAQ ANSWERS
# ==========================================================

faq_answers = {

    "How do I track my order?":
        "Customers can track orders from the My Orders page using the tracking ID provided after dispatch. "
        "Tracking updates are available in real time through our courier partners. "
        "An SMS and email notification with the tracking link is also sent once the order is dispatched.",

    "Can I cancel an order?":
        "Orders can be cancelled at any time before dispatch without any charges or penalties. "
        "Once dispatched, cancellation is not possible and customers must initiate a return after delivery. "
        "To cancel, visit the My Orders page or contact support between 9 AM and 9 PM IST.",

    "How do refunds work?":
        "Refunds are processed within 5 to 7 business days after the returned product passes quality inspection. "
        "The refund is credited to the original payment method used at checkout. "
        "UPI and bank transfer refunds may take an additional 2 to 3 working days depending on your bank. "
        "Products returned in a used, damaged, or incomplete condition may not qualify for a full refund.",

    "Do products come with warranty?":
        "Most ShopNova products include a standard one-year manufacturer warranty covering manufacturing defects. "
        "Premium products such as NovaBook Pro, NovaBook Ultra and Nova Studio Headphones include extended warranties of 2 to 5 years. "
        "Warranty does not cover physical damage, liquid damage, or unauthorised modifications. "
        "Warranty claims can be raised through the ShopNova warranty portal or by contacting customer support.",

    "Can I return opened products?":
        "Opened products may only be returned if they are defective, damaged upon delivery, or incorrectly sent. "
        "Products opened out of curiosity or change of mind are not eligible for return unless defective. "
        "Returns must be initiated within 30 days of delivery with the original packaging and all accessories included.",

    "What payment methods are accepted?":
        "ShopNova accepts UPI, debit cards, credit cards, net banking, EMI through supported banks, "
        "and cash on delivery for eligible orders. "
        "All online payments are secured through PCI-DSS compliant payment gateways. "
        "International cards may be subject to additional verification.",

    "How long does shipping take?":
        "Standard shipping takes 3 to 5 business days across most of India. "
        "Express shipping delivers within 1 to 2 business days in major cities including Mumbai, Delhi, Bengaluru, Hyderabad, Chennai and Pune. "
        "Remote and rural locations may require additional delivery time of 1 to 2 extra days. "
        "Tracking details are shared via SMS and email after dispatch.",

    "Do you ship across India?":
        "ShopNova delivers to most cities, towns and districts across India through trusted logistics partners. "
        "Some remote pin codes may have limited serviceability or longer delivery windows. "
        "You can check delivery availability by entering your pin code on the product page before placing an order.",

    "Can I exchange a product?":
        "Products can be exchanged within 7 days of delivery if they meet eligibility requirements. "
        "The item must be unused, in original packaging and accompanied by all accessories. "
        "Exchange requests can be raised through the My Orders section or by contacting support. "
        "The replacement unit is dispatched after the original item is picked up and inspected.",

    "What if I receive a damaged item?":
        "Customers should report damaged products within 48 hours of delivery by contacting support with photographs of the damage. "
        "ShopNova will arrange a free pickup and issue a replacement or full refund after verification. "
        "Do not discard the original packaging as it may be required during the pickup process.",

    "What if I receive the wrong item?":
        "Incorrectly delivered products qualify for a free replacement with priority dispatch. "
        "Please report the issue within 48 hours of delivery along with a photograph of the received item. "
        "ShopNova will arrange a free pickup of the wrong item and dispatch the correct product within 2 to 3 business days.",

    "Can I pay via EMI?":
        "EMI options are available for eligible products through supported credit cards and bank partners. "
        "No-cost EMI plans are available on select products for tenures of 3, 6 and 12 months. "
        "EMI availability is shown on the product page and confirmed at checkout based on your card and bank.",

    "Do you offer cash on delivery?":
        "Cash on delivery is available for selected products and serviceable pin codes. "
        "COD orders have a maximum order value limit. "
        "Availability is confirmed at checkout based on your delivery location and the product category.",

    "How do I contact support?":
        "ShopNova customer support is available through live chat, email and phone between 9 AM and 9 PM IST on all days. "
        "For faster resolution, use the live chat option on the website or app. "
        "Order-related queries can also be raised directly from the My Orders page.",

    "Can I update my delivery address?":
        "Delivery addresses can be updated before the order is dispatched through the My Orders page or by contacting support. "
        "Once the order has been dispatched, address changes are not possible. "
        "For urgent changes, contact support immediately with your order ID.",

    "When will my refund arrive?":
        "Refunds are typically processed within 5 to 7 business days after the return is approved. "
        "Credit card refunds may take an additional 3 to 5 business days to reflect depending on your bank. "
        "UPI refunds are usually faster and may reflect within 2 to 3 business days.",

    "Can I preorder products?":
        "Preorders are available for selected upcoming devices and launch editions. "
        "Preorder amounts are charged at the time of booking and the product is dispatched on or after the official launch date. "
        "Preorder customers receive priority dispatch and early delivery where available.",

    "Do you sell refurbished devices?":
        "ShopNova primarily sells brand new products with full manufacturer warranty. "
        "Certified refurbished products may occasionally be listed under a separate Refurbished section with clearly stated condition grades. "
        "All refurbished products undergo quality testing before listing.",

    "How does express shipping work?":
        "Express shipping prioritises order processing and reduces delivery time to 1 to 2 business days in supported cities. "
        "Express shipping is available at an additional fee shown at checkout. "
        "Orders placed before 12 PM are prioritised for same-day dispatch under the express plan.",

    "Do accessories have warranty?":
        "Most ShopNova accessories include a 6-month manufacturer warranty unless stated otherwise on the product page. "
        "Premium accessories such as the Nova Mechanical Keyboard and Nova USB-C Dock carry a 2-year warranty. "
        "Warranty claims for accessories follow the same process as other products through the warranty portal.",

    "Can businesses place bulk orders?":
        "Business customers can request volume pricing and quotations through ShopNova's enterprise sales team. "
        "Bulk orders may qualify for special pricing, priority fulfillment and dedicated account management. "
        "Contact the enterprise team through the Business Enquiry form on the website.",

    "How are returns inspected?":
        "Returned products undergo a quality inspection at the ShopNova fulfilment centre to verify condition, completeness and reported defects. "
        "Inspection typically takes 1 to 2 business days after the item is received. "
        "Refund or replacement is processed immediately after a successful inspection.",

    "What happens if delivery fails?":
        "If a delivery attempt fails, the courier will reattempt delivery on the next business day. "
        "After two failed attempts, the package is held at the nearest courier facility for 3 days before being returned to ShopNova. "
        "Customers can coordinate with support or the courier directly to reschedule delivery.",

    "Can I schedule delivery?":
        "Scheduled delivery is available in selected cities for eligible products. "
        "Customers can choose a preferred delivery date and time slot during checkout where the option is available. "
        "Rescheduling is also possible through the My Orders page before the order is out for delivery.",

    "How do I download invoices?":
        "Invoices are generated automatically once the order is delivered and can be downloaded from the My Orders section of your account. "
        "GST invoices are available for business purchases. "
        "If an invoice is missing or incorrect, contact support with your order ID for assistance.",

    "Do you sell TVs or home appliances?":
        "ShopNova specialises in personal electronics including laptops, smartphones, audio products, wearables and accessories. "
        "We do not currently carry televisions, home appliances, refrigerators, washing machines or furniture. "
        "Our catalogue is focused on portable and personal technology products.",

    "Do you sell gaming chairs or desks?":
        "ShopNova does not sell furniture including gaming chairs, desks or tables. "
        "We do carry electronics accessories relevant to gaming and desk setups such as the Nova Mechanical Keyboard, Nova Gaming Mouse, Nova Ergonomic Laptop Stand and Nova Laptop Cooling Pad.",

    "Do you sell cameras or DSLRs?":
        "ShopNova does not currently carry dedicated cameras, DSLRs or mirrorless cameras. "
        "We do carry smartphones with professional-grade camera systems such as the NovaPhone Edge with a 50MP Sony sensor and the NovaPhone Ultra with a 200MP main camera, which are suitable for most photography needs.",

    "Do you sell printers or scanners?":
        "ShopNova does not carry printers, scanners or multifunction devices. "
        "Our catalogue focuses on personal electronics including laptops, smartphones, audio, wearables and productivity accessories."

}


# ==========================================================
# POLICY ANSWERS
# ==========================================================

policy_answers = {

    "Refund Policy":
        "ShopNova processes refunds within 5 to 7 business days after the returned product passes quality inspection. "
        "Refunds are credited to the original payment method used at the time of purchase. "
        "UPI and bank transfer refunds may take an additional 2 to 3 working days depending on the customer's bank. "
        "Products returned in a damaged, used, or incomplete condition may not qualify for a full refund. "
        "Refund status can be tracked through the My Orders section.",

    "Return Policy":
        "Products may be returned within 30 days of delivery if unused and in original packaging with all accessories and documentation included. "
        "Opened products are eligible for return only if defective, damaged upon delivery, or incorrectly sent. "
        "Returns must be initiated through the My Orders page or by contacting customer support. "
        "ShopNova arranges a free pickup for eligible returns. "
        "Once the item is received and inspected, a refund or replacement is issued within 2 business days.",

    "Shipping Policy":
        "Standard shipping takes 3 to 5 business days across most of India. "
        "Express shipping is available in major cities and delivers within 1 to 2 business days at an additional charge. "
        "Free standard shipping applies to all orders above Rs 999. "
        "Tracking details are shared via SMS and email after dispatch. "
        "Remote and rural locations may experience delivery times of up to 7 business days.",

    "Warranty Policy":
        "Most ShopNova products include a standard one-year manufacturer warranty covering manufacturing defects and hardware failures under normal use. "
        "Premium products including select NovaBook laptops and NovaHead headphones carry extended warranties of 2 to 5 years as stated on the product page. "
        "Warranty does not cover physical damage, liquid damage, unauthorised repairs or modifications. "
        "Warranty claims must be raised through the ShopNova warranty portal with proof of purchase. "
        "On-site warranty service is available for select enterprise products.",

    "Cancellation Policy":
        "Orders may be cancelled at any time before dispatch without any penalty or cancellation fee. "
        "Once the order has been dispatched, cancellation is no longer possible and customers must wait for delivery to initiate a return. "
        "For prepaid orders, refunds after cancellation are processed within 5 to 7 business days to the original payment method. "
        "Partial cancellations are supported for orders containing multiple items where only some items have been dispatched.",

    "Exchange Policy":
        "Eligible products may be exchanged within 7 days of delivery for a different variant, colour or compatible model. "
        "The item must be unused, in original packaging and accompanied by all accessories and documentation. "
        "Exchange requests are raised through the My Orders section. "
        "ShopNova arranges pickup of the original item and dispatches the replacement after inspection. "
        "Price differences in exchanges are charged or refunded accordingly.",

    "COD Policy":
        "Cash on Delivery is available for selected products and serviceable pin codes across India. "
        "COD orders carry a maximum order value as displayed at checkout. "
        "Payment is collected by the delivery partner at the time of delivery. "
        "COD is not available for certain high-value products, pre-order items or express delivery orders.",

    "EMI Policy":
        "EMI options are available on eligible purchases through supported credit cards and bank partners at checkout. "
        "No-cost EMI plans are offered on select products for tenures of 3, 6 and 12 months. "
        "Standard EMI with applicable interest is available for longer tenures through partner banks. "
        "EMI availability depends on the customer's card issuer and is confirmed at the payment step.",

    "Privacy Policy":
        "ShopNova collects customer information solely for the purpose of processing orders, providing support and improving services. "
        "Customer data is never sold or shared with third parties for marketing purposes. "
        "All data is stored securely and handled in accordance with applicable data protection regulations. "
        "Customers may request deletion of their account and associated data by contacting support.",

    "Bulk Orders Policy":
        "Business customers and institutions can place bulk orders through ShopNova's enterprise sales channel. "
        "Bulk purchases of 5 units or more may qualify for volume pricing, dedicated account management and priority fulfillment. "
        "GST invoices are provided for all business orders. "
        "Enterprise enquiries can be submitted through the Business Orders form on the ShopNova website."

}


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    input_path = "data/shopnova_data.json"

    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found. Run generate_seed_data.py first.")
        exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    missing = []

    for item in data:

        if item["type"] == "faq":
            if item["title"] in faq_answers:
                item["content"] = faq_answers[item["title"]]
                updated += 1
            else:
                missing.append(f"[FAQ] {item['title']}")

        elif item["type"] == "policy":
            if item["title"] in policy_answers:
                item["content"] = policy_answers[item["title"]]
                updated += 1
            else:
                missing.append(f"[Policy] {item['title']}")

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    products = [i for i in data if i["type"] == "product"]
    faqs = [i for i in data if i["type"] == "faq"]
    policies = [i for i in data if i["type"] == "policy"]

    print(f"Dataset upgraded successfully — {updated} items updated")
    print(f"  Products : {len(products)}")
    print(f"  FAQs     : {len(faqs)}")
    print(f"  Policies : {len(policies)}")
    print(f"  Total    : {len(data)}")

    if missing:
        print(f"\nWARNING: {len(missing)} items had no answer match (check for title typos):")
        for m in missing:
            print(f"  - {m}")
    else:
        print("\nAll FAQs and policies matched and updated cleanly.")