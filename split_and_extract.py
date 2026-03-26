import os
import sys
from pypdf import PdfReader, PdfWriter
from loguru import logger
from agents.skill_extractor_agent import SkillExtractorAgent

def get_best_split_page(reader, total_pages):
    mid_point = total_pages // 2
    best_page = mid_point
    
    try:
        outlines = reader.outline
        if outlines:
            candidates = []
            for item in outlines:
                if isinstance(item, list):
                    continue
                try:
                    page_num = reader.get_destination_page_number(item)
                    candidates.append(page_num)
                except Exception:
                    pass
            
            # Find the candidate closest to mid_point
            if candidates:
                best_page = min(candidates, key=lambda x: abs(x - mid_point))
                logger.info(f"Trovato capitolo alla pagina {best_page} dal sommario.")
                return best_page
    except Exception as e:
        logger.warning(f"Errore lettura outline: {e}")
        
    logger.warning("Nessun sommario trovato, split fallback alla pagina esatta di metà (che potrebbe tagliare un pattern a metà).")
    return best_page

def main():
    original_pdf = "/Users/gpp/Programmazione/Trading/In Lavorazione/Trading_AI_App v2/data/books/Encyclopedia Of Chart Patterns, 2nd Edition.pdf"
    
    if not os.path.exists(original_pdf):
        logger.error(f"File non trovato: {original_pdf}")
        return
        
    reader = PdfReader(original_pdf)
    total_pages = len(reader.pages)
    logger.info(f"Il PDF contiene {total_pages} pagine.")
    
    split_page = get_best_split_page(reader, total_pages)
    
    vol1_path = original_pdf.replace(".pdf", " - Vol 1.pdf")
    vol2_path = original_pdf.replace(".pdf", " - Vol 2.pdf")
    
    logger.info(f"Divido il documento alla pagina {split_page}...")
    
    if not os.path.exists(vol1_path) or not os.path.exists(vol2_path):
        writer1 = PdfWriter()
        for i in range(split_page):
            writer1.add_page(reader.pages[i])
        with open(vol1_path, "wb") as f_out:
            writer1.write(f_out)
            
        writer2 = PdfWriter()
        for i in range(split_page, total_pages):
            writer2.add_page(reader.pages[i])
        with open(vol2_path, "wb") as f_out:
            writer2.write(f_out)
    
    logger.info("PDF Diviso! Inizio l'estrazione Agentic...")
    
    agent = SkillExtractorAgent()
    
    logger.info(f"--- VOL 1 ({split_page} pagine) ---")
    gemini_v1 = agent.upload_book(vol1_path)
    md_v1 = agent.extract_skills_da_file(gemini_v1)
    
    logger.info(f"--- VOL 2 ({total_pages - split_page} pagine) ---")
    gemini_v2 = agent.upload_book(vol2_path)
    md_v2 = agent.extract_skills_da_file(gemini_v2)
    
    combined_md = f"Parte 1:\\n{md_v1}\\n\\n---\\n\\nParte 2:\\n{md_v2}"
    agent.save_skills_as_markdown(combined_md, "Encyclopedia Of Chart Patterns")
    logger.info("Estrazione combinata SUCCESS!")

if __name__ == "__main__":
    main()
