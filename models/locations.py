class Locations:
    glasgow_accepted_zip_codes = (
        # City Centre & Central Areas
        ("G1", "Glasgow City Centre - Merchant City"),
        ("G2", "Glasgow City Centre - Financial District"),
        ("G3", "Charing Cross, Anderston, Finnieston, Yorkhill"),
        ("G4", "Glasgow Cathedral, Townhead, Cowcaddens"),
        # West End
        ("G11", "Partick, Thornwood"),
        ("G12", "Hillhead, Dowanhill, University of Glasgow"),
        ("G13", "Anniesland, Jordanhill"),
        ("G14", "Whiteinch, Scotstoun"),
        ("G20", "Maryhill, North Kelvinside"),
        # Southside
        ("G41", "Pollokshields, Strathbungo, Shawlands"),
        ("G42", "Govanhill, Battlefield"),
        ("G43", "Pollokshaws, Auldhouse"),
        ("G44", "Cathcart, Mount Florida"),
        ("G51", "Govan, Ibrox"),
        ("G52", "Cardonald, Hillington"),
        # East End
        ("G31", "Dennistoun, Haghill"),
        ("G32", "Carmyle, Mount Vernon"),
        ("G40", "Bridgeton, Dalmarnock"),
        # North Glasgow
        ("G21", "Springburn, Sighthill"),
        ("G22", "Possilpark, Parkhouse"),
        # Surrounding Areas
        ("G61", "Bearsden"),
        ("G62", "Milngavie"),
        ("G64", "Bishopbriggs"),
        ("G71", "Uddingston"),
        ("G72", "Cambuslang"),
        ("G73", "Rutherglen"),
        ("G74", "East Kilbride"),
        ("G76", "Clarkston, Busby"),
    )
    current_location = None

    def __init__(self, location):
        self.current_location = location

    def get_all_locations(self):
        return self.glasgow_accepted_zip_codes

    def get_current_location(self):
        return self.current_location

    def set_current_location(self, new_location):
        self.current_location = new_location
