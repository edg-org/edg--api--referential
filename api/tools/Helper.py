# Function to generate geographical natural zone code
def generate_zone_code(code: int):
    return code+10

# Function to generate administrative region base code
def region_basecode(code: int):
    return code*10

# Function to generate prefecture base code
def prefecture_basecode(code: int):
    return code*100

# Function to generate city base code
def city_basecode(code: int):
    return code*100
    
# Function to generate area base code
def area_basecode(code: int):
    return code*100
    
# Function to generate street base code
def agency_basecode(code: int):
    code+1
    
# Function to generate address code
def address_basecode(code: int):
    return code*100

# Function to generate zipcode
def generate_zipcode(zipcode_base: int, step: int):
    return str(zipcode_base+step).zfill(5)