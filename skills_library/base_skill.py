class BaseTradingSkill:
    """
    Classe base per standardizzare le regole di trading astratte (Skill).
    Garantisce che ogni skill possa conservare memoria della sua origine
    per approfondimenti futuri tramite Agentic File Search di Gemini.
    """
    def __init__(self, 
                 nome: str, 
                 descrizione: str, 
                 logica: str, 
                 source_context: str = "", 
                 source_file_uri: str = "", 
                 source_book: str = ""):
        self.nome = nome
        self.descrizione = descrizione
        self.logica = logica
        self.source_context = source_context
        self.source_file_uri = source_file_uri
        self.source_book = source_book

    def to_dict(self):
        """ serializza la skill in formato dizionario """
        return {
            "nome": self.nome,
            "descrizione": self.descrizione,
            "logica": self.logica,
            "source_context": self.source_context,
            "source_file_uri": self.source_file_uri,
            "source_book": self.source_book
        }

    def __repr__(self):
        return f"<BaseTradingSkill: {self.nome} - {self.source_book}>"
