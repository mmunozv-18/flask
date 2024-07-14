from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Obtener datos del formulario
        data = {
            "name": request.form.get("name", ""),
            "organization": request.form.get("organization", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "note": request.form.get("note", "")
        }

        # Crear el contenido de la vCard
        vcard_content = f"BEGIN:VCARD\nVERSION:3.0\n"
        vcard_content += f"FN:{data['name']}\n"
        vcard_content += f"ORG:{data['organization']}\n"
        vcard_content += f"EMAIL:{data['email']}\n"
        vcard_content += f"TEL:{data['phone']}\n"
        vcard_content += f"NOTE:{data['note']}\n"
        vcard_content += "END:VCARD"

        # Generar QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(vcard_content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="Green", back_color="white")
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Enviar imagen como respuesta para descargar
        return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name='vcard_qr.png')

    # Mostrar la página con el formulario si es GET
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)