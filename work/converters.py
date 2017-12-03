
def convert_work_to_dict(work):
    return {
        "id": work.id,
        "description": work.description,
        "time": str(work.time),
        "images": convert_images_to_dict(work.images),
        "worktype": convert_work_type_to_dict(work.worktype),
        "address": convert_address_to_dict(work.address),
        "state": work.state,
        "worker": convert_worker_to_dict(work.worker)
    }
def convert_worker_to_dict(worker):
    if worker is None:
        return None
    return {
        "username": worker.user.username,
        "first_name": worker.user.first_name,
        "last_name": worker.user.last_name,
        "email": worker.user.email,
        "phone": worker.phone,
        "profile_pic": str(worker.profile_pic.url),
        "rh": worker.rh,
        "document_id": worker.document_id
    }

def convert_address_to_dict(address):
    if address is None:
        return None
    return {
        "id": address.id,
        "name": address.name,
        "address": address.address,
        "city": address.city,
        "country": address.country,
        "latitude": address.latitude,
        "longitude": address.longitude
    }
def convert_work_type_to_dict(worktype):
    if worktype is None:
        return None
    return {
        "id": worktype.id,
        "name": worktype.name,
        "description": worktype.description,
        "icon": str(worktype.icon.url),
        "price_type": worktype.price_type,
        "price": worktype.price,
        "order": worktype.order
    }

def convert_images_to_dict(images):
    if images is None:
        return None
    image_list = []
    print("returning image list")
    for image in images.all():
        image_list.append(str(image.image.url))
    return image_list
