from flask import Flask, render_template, request, send_from_directory
from datetime import date, datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Frame, KeepInFrame
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

@app.route("/")
def index():
    request_date = request.args.get('date')
    print(request_date)
    today = date.today()
    apikey = "VIHpJnZbDy6lraMNDzVHGsKTXMHMn3vgIC5Cu8FV"

    if not request_date:
        return render_template('index.html', request_date=today.strftime("%Y-%m-%d"), apikey=apikey, pdf=getPDF)
    
    try:
        request_date = datetime.strptime(request_date, "%Y-%m-%d").date()
    except ValueError:
        return "404, NASA Astronomy Picture of the Day could not be found for this date", 404

    if request_date <= today:
        return render_template('index.html', request_date=request_date.strftime("%Y-%m-%d"), apikey=apikey, pdf=getPDF)    
    else:
        return "404, NASA Astronomy Picture of the Day could not be found for this date", 404

@app.route('/data/output.pdf')
def getPDF():
    url = request.args.get("url")
    description = request.args.get("desc")
    image = ImageReader(url)
    c = canvas.Canvas('data/output.pdf', pagesize=letter)
    c.drawImage(image, 100, 325, width=400, height=400, mask='auto')
    frame1 = Frame(0.25*inch, 0.25*inch, 8*inch, 4*inch, showBoundary=1)
    styles = getSampleStyleSheet()
    para = [Paragraph("Description: "+description, styles['Normal'])]
    para_inframe = KeepInFrame(8*inch, 8*inch, para)
    frame1.addFromList([para_inframe], c)
    c.save()
    return send_from_directory('data', "output.pdf")

if __name__ == '__main__':
     app.run(port=80, debug=False)