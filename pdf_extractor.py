import flet as ft
import pandas as pd
import pdfplumber
from pathlib import Path
import io

class PDFtoCSVExtractor:
    def __init__(self):
        self.pdf_path = None
        self.extracted_data = None
        
    def extract_from_pdf(self, pdf_path):
        """Extract tables and text from PDF"""
        all_tables = []
        all_text = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if table:
                            all_tables.append(table)
                
                # Extract text as fallback
                text = page.extract_text()
                if text:
                    all_text.append(text)
        
        return all_tables, all_text
    
    def clean_and_convert(self, tables, text_data):
        """Clean data and convert to DataFrame"""
        if tables:
            # Process first table (you can modify to handle multiple tables)
            df = pd.DataFrame(tables[0])
            
            # Use first row as header if it looks like headers
            if len(df) > 0:
                df.columns = df.iloc[0]
                df = df[1:]
                df.reset_index(drop=True, inplace=True)
            
            # Clean data
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df = df.replace('', pd.NA)
            
            return df
        elif text_data:
            # If no tables, try to parse text as CSV-like data
            lines = text_data[0].split('\n')
            data = [line.split() for line in lines if line.strip()]
            return pd.DataFrame(data)
        
        return None

def main(page: ft.Page):
    page.title = "PDF to CSV Extractor"
    page.window_width = 700
    page.window_height = 600
    page.padding = 20
    
    extractor = PDFtoCSVExtractor()
    
    # UI Components
    file_path_text = ft.Text("No file selected", size=14, color=ft.Colors.GREY_700)
    status_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    preview_text = ft.Text("", size=12, selectable=True)
    
    def pick_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            file_path_text.value = f"Selected: {Path(file_path).name}"
            extractor.pdf_path = file_path
            status_text.value = ""
            preview_text.value = ""
            extract_btn.disabled = False
            page.update()
    
    def extract_data(e):
        if not extractor.pdf_path:
            status_text.value = "❌ Please select a PDF file first"
            status_text.color = ft.Colors.RED
            page.update()
            return
        
        try:
            status_text.value = "⏳ Extracting data..."
            status_text.color = ft.Colors.BLUE
            page.update()
            
            tables, text_data = extractor.extract_from_pdf(extractor.pdf_path)
            
            if not tables and not text_data:
                status_text.value = "❌ No data found in PDF"
                status_text.color = ft.Colors.RED
                page.update()
                return
            
            df = extractor.clean_and_convert(tables, text_data)
            
            if df is not None and not df.empty:
                extractor.extracted_data = df
                status_text.value = f"✅ Extracted {len(df)} rows × {len(df.columns)} columns"
                status_text.color = ft.Colors.GREEN
                
                # Show preview
                preview_text.value = f"Preview:\n{df.head(10).to_string()}"
                
                export_btn.disabled = False
            else:
                status_text.value = "❌ Could not parse data from PDF"
                status_text.color = ft.Colors.RED
            
            page.update()
            
        except Exception as ex:
            status_text.value = f"❌ Error: {str(ex)}"
            status_text.color = ft.Colors.RED
            page.update()
    
    def save_file_result(e: ft.FilePickerResultEvent):
        if e.path and extractor.extracted_data is not None:
            try:
                output_path = e.path
                if not output_path.endswith('.csv'):
                    output_path += '.csv'
                
                extractor.extracted_data.to_csv(output_path, index=False)
                status_text.value = f"✅ Saved to: {Path(output_path).name}"
                status_text.color = ft.Colors.GREEN
                page.update()
            except Exception as ex:
                status_text.value = f"❌ Save error: {str(ex)}"
                status_text.color = ft.Colors.RED
                page.update()
    
    # File pickers
    pick_file_dialog = ft.FilePicker(on_result=pick_file_result)
    save_file_dialog = ft.FilePicker(on_result=save_file_result)
    page.overlay.extend([pick_file_dialog, save_file_dialog])
    
    # Buttons
    select_btn = ft.ElevatedButton(
        "Select PDF File",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: pick_file_dialog.pick_files(
            allowed_extensions=["pdf"],
            dialog_title="Select PDF file"
        )
    )
    
    extract_btn = ft.ElevatedButton(
        "Extract Data",
        icon=ft.icons.TRANSFORM,
        on_click=extract_data,
        disabled=True
    )
    
    export_btn = ft.ElevatedButton(
        "Export to CSV",
        icon=ft.icons.SAVE,
        on_click=lambda _: save_file_dialog.save_file(
            file_name="extracted_data.csv",
            allowed_extensions=["csv"],
            dialog_title="Save CSV file"
        ),
        disabled=True
    )
    
    # Layout
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("PDF to CSV Extractor", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Container(height=10),
                select_btn,
                file_path_text,
                ft.Container(height=20),
                extract_btn,
                ft.Container(height=10),
                status_text,
                ft.Container(height=20),
                export_btn,
                ft.Container(height=20),
                ft.Container(
                    content=preview_text,
                    bgcolor=ft.Colors.GREY_100,
                    padding=10,
                    border_radius=5,
                    expand=True
                )
            ], scroll=ft.ScrollMode.AUTO),
            expand=True
        )
    )

if __name__ == "__main__":
    # Use web mode to avoid desktop dependencies
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550)