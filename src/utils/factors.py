"""
Comprehensive CO2 emission factors for various environmental activities.
All factors are in kg CO2 saved per unit.
"""

FACTORS = {
    # Transportation factors (kg CO2 per km)
    'car_kg_per_km': 0.12,
    'taxi_kg_per_km': 0.15,
    'motorcycle_kg_per_km': 0.08,
    'bus_kg_per_km': 0.089,
    'train_kg_per_km': 0.041,
    'metro_kg_per_km': 0.028,
    'airplane_kg_per_km': 0.255,  # domestic flights
    'walk_kg_per_km': 0.0,
    'cycle_kg_per_km': 0.0,
    'electric_vehicle_kg_per_km': 0.045,
    'scooter_kg_per_km': 0.015,
    'carpool_kg_per_km': 0.06,  # car emissions divided by avg passengers
    
    # Transportation per trip (kg CO2 saved per trip)
    'walk_trip_vs_car': 2.4,  # avg 2km car trip saved
    'cycle_trip_vs_car': 3.6,  # avg 3km car trip saved  
    'bus_trip_vs_car': 1.8,   # avg short trip
    'train_trip_vs_car': 6.0, # avg longer trip
    
    # Energy factors (kg CO2 per unit)
    'led_bulb_vs_incandescent_per_hour': 0.04,  # per hour of use
    'unplug_device_per_hour': 0.02,  # standby power saved
    'air_dry_vs_dryer_per_load': 2.3,
    'energy_efficient_appliance_per_hour': 0.15,
    'solar_panel_per_kwh': 0.82,  # vs grid electricity
    'shorter_shower_per_minute': 0.17,  # 1 min less hot water
    
    # Food factors (kg CO2 per meal/portion)
    'meal_beef_to_veg_kg': 7.0,
    'meal_chicken_to_veg_kg': 1.5,
    'meal_pork_to_veg_kg': 3.5,
    'vegan_meal_vs_omnivore': 2.5,  # average meal
    'local_food_vs_imported_kg': 0.8,  # per kg of food
    'organic_vs_conventional_kg': 0.3,  # per kg of food
    'reduce_food_waste_per_kg': 3.3,  # food waste avoided
    
    # Waste factors (kg CO2 per item/kg)
    'plastic_bottle_kg': 0.1,
    'recycle_vs_trash_per_kg': 1.1,
    'compost_vs_trash_per_kg': 0.35,
    'reuse_item_vs_new': 2.0,  # average item
    'cloth_bag_vs_plastic': 0.006,  # per use
    'repair_vs_replace_electronics': 50.0,  # average device
    'repair_vs_replace_clothing': 8.0,   # average garment
    
    # Water factors (kg CO2 per liter/minute)
    'water_heating_per_liter': 0.0036,
    'shorter_shower_per_minute_saved': 0.17,
    'fix_leak_per_liter_per_day': 0.0036,
    'dishwasher_efficient_per_load': 0.9,
    'rain_water_per_liter': 0.0036,  # vs tap water
    
    # Other environmental actions
    'plant_tree_lifetime_kg': 22.0,  # CO2 absorbed over lifetime
    'work_from_home_per_day': 4.6,  # commute avoided
    'green_product_vs_conventional': 1.5,  # average product
    'sustainable_fashion_vs_fast': 15.0,  # per garment
    'digital_receipt_vs_paper': 0.003,
    'e_book_vs_physical': 7.5,  # per book
    'streaming_vs_dvd_per_hour': 0.0036,
    
    # Digital environmental actions
    'smartphone_usage_per_hour': 0.0088,  # average smartphone energy consumption
    'digital_detox_per_hour': 0.0088,     # energy saved by not using phone
    'reduce_screen_time_per_hour': 0.0088, # energy saved
    'wifi_router_per_hour': 0.006,        # router energy usage
    'data_center_per_gb': 0.0036,         # cloud service energy
    'email_per_message': 0.0000041,       # email carbon footprint
}

# Category-based default factors for unknown activities
DEFAULT_FACTORS = {
    'transportation': 2.0,  # default trip savings
    'energy': 1.0,         # default energy savings
    'food': 2.0,           # default meal savings
    'waste': 0.5,          # default waste item
    'water': 0.2,          # default water savings
    'digital': 0.2,        # default digital activity savings
    'other': 1.0,          # default other activity
}

def get_co2_factor(action: str, category: str, instead_of: str = None) -> float:
    """
    Get CO2 emission factor for an activity.
    
    Args:
        action: Specific action taken
        category: Category of the action
        instead_of: What conventional activity was replaced
        
    Returns:
        CO2 factor in kg per unit
    """
    # Try direct action lookup first
    direct_key = f"{action}_kg_per_unit"
    if direct_key in FACTORS:
        return FACTORS[direct_key]
    
    # Try action vs instead_of lookup
    if instead_of:
        vs_key = f"{action}_vs_{instead_of}"
        if vs_key in FACTORS:
            return FACTORS[vs_key]
        
        # Try per km for transportation
        if category == 'transportation':
            action_factor = FACTORS.get(f"{action}_kg_per_km", 0.0)
            instead_factor = FACTORS.get(f"{instead_of}_kg_per_km", 0.0)
            if action_factor >= 0 and instead_factor > 0:
                return instead_factor - action_factor
    
    # Try category-specific patterns
    if category == 'transportation':
        # Transportation per km
        per_km_key = f"{action}_kg_per_km"
        if per_km_key in FACTORS:
            if instead_of:
                instead_km_key = f"{instead_of}_kg_per_km"
                if instead_km_key in FACTORS:
                    return FACTORS[instead_km_key] - FACTORS[per_km_key]
            return FACTORS.get('car_kg_per_km', 0.12)  # default vs car
            
        # Transportation per trip
        per_trip_key = f"{action}_trip_vs_car"
        if per_trip_key in FACTORS:
            return FACTORS[per_trip_key]
    
    elif category == 'food':
        # Food meal patterns
        if 'meal' in action or 'vegetarian' in action or 'vegan' in action:
            if instead_of and f"meal_{instead_of}_to_veg_kg" in FACTORS:
                return FACTORS[f"meal_{instead_of}_to_veg_kg"]
            return FACTORS.get('meal_chicken_to_veg_kg', 1.5)
        
        # Food per kg patterns  
        vs_key = f"{action}_vs_conventional_kg"
        if vs_key in FACTORS:
            return FACTORS[vs_key]
    
    elif category == 'waste':
        # Waste-specific patterns
        if 'recycle' in action:
            return FACTORS.get('recycle_vs_trash_per_kg', 1.1)
        elif 'reuse' in action:
            return FACTORS.get('reuse_item_vs_new', 2.0)
        elif 'bottle' in action:
            return FACTORS.get('plastic_bottle_kg', 0.1)
    
    elif category == 'energy':
        # Energy-specific patterns
        if 'led' in action or 'bulb' in action:
            return FACTORS.get('led_bulb_vs_incandescent_per_hour', 0.04)
        elif 'unplug' in action:
            return FACTORS.get('unplug_device_per_hour', 0.02)
        elif 'solar' in action:
            return FACTORS.get('solar_panel_per_kwh', 0.82)
    
    elif category == 'water':
        # Water-specific patterns
        if 'shower' in action:
            return FACTORS.get('shorter_shower_per_minute_saved', 0.17)
        return FACTORS.get('water_heating_per_liter', 0.0036)
    
    elif category == 'digital':
        # Digital wellness patterns
        if 'detox' in action or 'did not use' in action or 'avoid' in action:
            return FACTORS.get('digital_detox_per_hour', 0.0088)
        elif 'reduce' in action or 'less' in action:
            return FACTORS.get('reduce_screen_time_per_hour', 0.0088)
        elif 'smartphone' in action or 'phone' in action:
            return FACTORS.get('smartphone_usage_per_hour', 0.0088)
        return FACTORS.get('digital_detox_per_hour', 0.0088)
    
    # Return default factor for category
    return DEFAULT_FACTORS.get(category, 1.0)
