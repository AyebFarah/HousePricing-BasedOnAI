import numpy as np

def engineer_features(data):
    data['room_bathroom_ratio'] = data['room_count'] / np.maximum(data['bathroom_count'], 1)
    data['total_rooms'] = data['room_count'] + data['bathroom_count']
    data['size_per_room'] = data['size'] / np.maximum(data['room_count'], 1)
    data['bathroom_density'] = data['bathroom_count'] / np.maximum(data['size'], 1)
    data['size_x_rooms'] = data['size'] * data['room_count']
    data['size_x_bathrooms'] = data['size'] * data['bathroom_count']

    for col in ['room_bathroom_ratio', 'total_rooms', 'size_per_room', 
                'bathroom_density', 'size_x_rooms', 'size_x_bathrooms']:
        data[col] = data[col].replace([np.inf, -np.inf], np.nan).fillna(data[col].median())

    return data