import phonenumbers
from phonenumbers import geocoder, carrier, phonenumberutil, timezone

# Header Design
title = """
===========================================
  🌐 Phone Number Details Extractor 🌐
===========================================
"""
print("\033[1;36m" + title + "\033[m")

print("Welcome to the Phone Number Details Extractor!")
print("Please enter a phone number (with country code, e.g., +1XXXXXXXXXX):")

# Input from the user
phone_number = input("Enter the phone number: ")


def extract_phone_details(phone_number):
    try:
        # Parse the phone number
        number = phonenumbers.parse(phone_number, None)

        # Validate the number
        validity = "Valid" if phonenumbers.is_valid_number(number) else "Invalid"
        if validity == "Invalid":
            return {"Error": "The phone number entered is invalid. Please try again."}

        # Extract details
        country_code = phonenumbers.region_code_for_number(number)
        country_name = geocoder.country_name_for_number(number, "en")
        location = geocoder.description_for_number(number, "en") or "Unknown Location"
        carrier_name = carrier.name_for_number(number, "en") or "Unknown Carrier"
        number_type = phonenumbers.number_type(number)
        number_type_description = {
            phonenumbers.PhoneNumberType.MOBILE: "Mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "Fixed-line",
            phonenumbers.PhoneNumberType.VOIP: "VOIP",
            phonenumbers.PhoneNumberType.TOLL_FREE: "Toll-free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "Premium rate"
        }.get(number_type, "Other")

        time_zones = timezone.time_zones_for_number(number)
        time_zones_description = ", ".join(time_zones) if time_zones else "Time zone information not available"

        formatted_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)
        e164_format = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        rfc3966_format = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.RFC3966)
        national_significant_number = phonenumbers.national_significant_number(number)

        # Check additional properties
        valid_in_region = phonenumbers.is_valid_number_for_region(number, country_code)
        is_possible_number = "Possible" if phonenumbers.is_possible_number(number) else "Not possible"
        is_possible_mobile = "Possible" if phonenumbers.is_possible_number_for_type(number,
                                                                                    phonenumbers.PhoneNumberType.MOBILE) else "Not possible"
        is_possible_short_code = "Possible" if phonenumbers.is_possible_short_number(number) else "Not possible"
        possible_emergency_number = "Yes" if phonenumbers.is_possible_number_for_type(number,
                                                                                      phonenumbers.PhoneNumberType.FIXED_LINE) else "No"

        # Dummy latitude, longitude, administrative area (not supported by phonenumbers)
        latitude = None
        longitude = None
        administrative_area = None
        possible_geocoding = None

        # Compile details into a dictionary
        details = {
            "Country Code": country_code,
            "Country Name": country_name,
            "Location": location,
            "Latitude": latitude,
            "Longitude": longitude,
            "Administrative Area": administrative_area,
            "Possible Geocoding (US)": possible_geocoding,
            "Sim Name": carrier_name,
            "Number Type": number_type_description,
            "Validity": validity,
            "Valid in Region": valid_in_region,
            "Formatted Number": formatted_number,
            "Possible Lengths": len(phone_number),
            "Is Possible Number": is_possible_number,
            "Time Zones": time_zones_description,
            "National Number": national_number,
            "Extension": "No extension",
            "Possible Emergency Number": possible_emergency_number,
            "Possible Mobile Number": is_possible_mobile,
            "Possible Short Code": is_possible_short_code,
            "Valid Number in Region": "Valid" if valid_in_region else "Not valid",
            "Time Zone Name": time_zones_description,
            "National Significant Number": national_significant_number,
            "E164 Format": e164_format,
            "RFC3966 Format": rfc3966_format,
            "Possible Types": number_type
        }
        return details

    except phonenumbers.phonenumberutil.NumberParseException as e:
        return {"Error": f"Number could not be parsed: {e}"}


# Extract details
details = extract_phone_details(phone_number)

# Display details
if "Error" in details:
    print("\n❌", details["Error"])
else:
    print("\n🌐 Phone Number Details 🌐")
    for key, value in details.items():
        print(f"{key}: {value}")

print("\nThank you for using the Phone Number Details Extractor!")
print("===========================================\n")
