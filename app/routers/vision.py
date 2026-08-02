from fastapi import APIRouter, File, HTTPException, UploadFile

from app.database import CustomerVisit, SessionLocal
from app.services.cv_utils import read_image_from_bytes
from app.services.face_service import load_face_recognizer, recognize_face
from app.services.product_service import load_product_model, predict_product

router = APIRouter()

product_model = load_product_model()
face_recognizer, label_to_customer = load_face_recognizer()


@router.get("/classify-product")
def classify_product():
    return {
        "message": "Product classification endpoint is ready"
    }


@router.post("/classify-product")
async def upload_product_image(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    image_bytes = await file.read()

    try:
        image = read_image_from_bytes(image_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return predict_product(image, product_model)


@router.post("/recognize-face")
async def recognize_customer_face(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    image_bytes = await file.read()

    try:
        image = read_image_from_bytes(image_bytes)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    result = recognize_face(image, face_recognizer, label_to_customer)

    database = SessionLocal()

    try:
        database.add(
            CustomerVisit(
                customer_id=result["customer_id"],
                status=result["status"],
                distance=result["distance"],
            )
        )
        database.commit()
    finally:
        database.close()

    return result