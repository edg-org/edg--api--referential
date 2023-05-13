# Function to generate geographical natural zone code
def generate_zone_code(code: int):
    return code+10

# Function to generate administrative region base code
def region_basecode(code: int) -> int:
    return code*10

# Function to generate prefecture base code
def prefecture_basecode(code: int) -> int:
    return code*100

# Function to generate city base code
def city_basecode(code: int):
    return code*100
    
# Function to generate area base code
def area_basecode(code: int)-> int:
    return code*100
    
# Function to generate agency base code
def agency_basecode(code: int) -> int:
    return code*10

# Function to generate street code
def street_basecode(code: int) -> int:
    return code*100

# Function to generate address code
def address_basecode(code: int) -> int:
    return code*100

# Function to generate delivery point code
def deliverypoint_basecode(code: int) -> int:
    return code*10000

# Function to generate energy supply line base code
def supply_basecode(code: int)-> int:
    return code*100

# Function to generate transformer base code
def transformer_basecode(code: int)-> int:
    return code*100

# Function to generate connection point base code
def connectionpoint_basecode(code: int)-> int:
    return code*100

# Function to generate zipcode
def generate_zipcode(zipcode_base: int, step: int) -> str:
    return str(zipcode_base+step).zfill(5)

# function to generate code
def generate_code(
    init_codebase : int,
    maxcode :int, 
    step: int
) -> int:
    if maxcode > 0:
        basecode = maxcode
    else:
        basecode = init_codebase

    return dict(step=step, code=(basecode+step))