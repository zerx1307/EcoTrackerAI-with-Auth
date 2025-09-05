def equivalents(kg: float):
    if kg <= 0:
        return {'phone_charges': 0, 'lightbulb_hours': 0, 'trees_year': 0.0}
    phone_charges = int(kg * 50)
    lightbulb_hours = int(kg * 10)
    trees_year = round(kg / 21.0, 3)
    return {'phone_charges': phone_charges, 'lightbulb_hours': lightbulb_hours, 'trees_year': trees_year}
