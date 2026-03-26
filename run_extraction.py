import os
from agents.skill_extractor_agent import SkillExtractorAgent
from loguru import logger

def main():
    # Nuovo libro inserito dall'utente per l'estrazione Agentic
    filepath = "/Users/gpp/Programmazione/Trading/In Lavorazione/Trading_AI_App v2/data/books/Joe Ross - Daytrading (Merged Clean).pdf"
    
    logger.info("Inizializzazione SkillExtractorAgent...")
    agent = SkillExtractorAgent()
    
    try:
        logger.info(f"Caricamento PDF: {filepath}")
        gemini_f = agent.upload_book(filepath)
        logger.info("PDF caricato. Inizio estrazione testo Markdown skills...")
        extracted_md = agent.extract_skills_da_file(gemini_f)
        
        if extracted_md:
            logger.info("Procedo al salvataggio del volume completo in markdown...")
            book_title = gemini_f.display_name if gemini_f.display_name else "Volume_Trading"
            agent.save_skills_as_markdown(extracted_md, book_title)
            logger.info("✅ Operazione conclusa con successo!")
        else:
            logger.warning("Risultato vuoto dall'LLM.")
            
    except Exception as e:
        logger.error(f"Esecuzione interrotta per errore: {e}")

if __name__ == "__main__":
    main()
