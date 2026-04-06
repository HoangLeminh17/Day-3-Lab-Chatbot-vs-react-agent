def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """
    Chuyển đổi giữa các đơn vị đo lường nhà bếp như gram, cup, ml, muỗng cà phê, vv.
    
    Args:
        value: Giá trị cần chuyển đổi.
        from_unit: Đơn vị nguồn (ví dụ: 'gram', 'cup', 'ml', 'tsp').
        to_unit: Đơn vị đích (ví dụ: 'gram', 'cup', 'ml', 'tsp').
        
    Returns:
        Chuỗi kết quả chuyển đổi hoặc thông báo lỗi.
    """
    # Normalize units
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    # Define conversion factors to a base unit (Weight: gram, Volume: ml)
    # Note: For cross-conversion (weight <-> volume), we assume density of water (1g = 1ml)
    
    weight_units = {
        'g': 1.0,
        'gram': 1.0,
        'grams': 1.0,
        'kg': 1000.0,
        'kilogram': 1000.0,
        'kilograms': 1000.0,
        'oz': 28.35,
        'ounce': 28.35,
        'ounces': 28.35,
        'lb': 453.59,
        'pound': 453.59,
        'pounds': 453.59,
    }
    
    volume_units = {
        'ml': 1.0,
        'milliliter': 1.0,
        'milliliters': 1.0,
        'l': 1000.0,
        'liter': 1000.0,
        'liters': 1000.0,
        'cup': 240.0,
        'cups': 240.0,
        'tbsp': 15.0,
        'tablespoon': 15.0,
        'tablespoons': 15.0,
        'muỗng canh': 15.0,
        'tsp': 5.0,
        'teaspoon': 5.0,
        'teaspoons': 5.0,
        'muỗng cà phê': 5.0,
        'fl oz': 29.57,
        'fluid ounce': 29.57,
        'fluid ounces': 29.57,
    }

    # Combined units for easier lookup (assuming 1g = 1ml for kitchen simplicity)
    all_units = {**weight_units, **volume_units}

    if from_unit not in all_units:
        # Try stripping 's' if not found
        if from_unit.endswith('s') and from_unit[:-1] in all_units:
            from_unit = from_unit[:-1]
        else:
            return f"Error: Đơn vị '{from_unit}' không được hỗ trợ."
            
    if to_unit not in all_units:
        # Try stripping 's' if not found
        if to_unit.endswith('s') and to_unit[:-1] in all_units:
            to_unit = to_unit[:-1]
        else:
            return f"Error: Đơn vị '{to_unit}' không được hỗ trợ."

    # Convert to base unit (ml or g)
    base_value = value * all_units[from_unit]
    
    # Convert from base unit to target unit
    converted_value = base_value / all_units[to_unit]
    
    return f"{value} {from_unit} = {converted_value:.2f} {to_unit}"
