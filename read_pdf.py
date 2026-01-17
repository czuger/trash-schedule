import PyPDF2
import re


def read_pdf_content(pdf_path):
    """
    Lit et affiche le contenu texte d'un PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            print(f"=== INFOS DU PDF ===")
            print(f"Nombre de pages: {len(pdf_reader.pages)}")
            print(f"Métadonnées: {pdf_reader.metadata}")
            print("=" * 50 + "\n")

            # Lire chaque page
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()

                print(f"\n{'=' * 60}")
                print(f"PAGE {page_num}")
                print(f"{'=' * 60}")

                # Afficher le texte de la page
                print(text)

                # Optionnel: Afficher un résumé de la page
                words = text.split()
                print(f"\n[Page {page_num}: {len(words)} mots, {len(text)} caractères]")

                # Chercher des patterns intéressants
                find_patterns_in_page(text, page_num)

    except FileNotFoundError:
        print(f"ERREUR: Le fichier '{pdf_path}' n'existe pas.")
    except Exception as e:
        print(f"ERREUR: {e}")


def find_patterns_in_page(text, page_num):
    """
    Cherche et affiche des patterns intéressants dans le texte
    """
    patterns = {
        "Dates": r'\b\d{1,2}\s+\w+\s+\d{4}\b|\b\d{1,2}/\d{1,2}/\d{4}\b',
        "Jours de la semaine": r'\b(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|Lu|Ma|Me|Je|Ve|Sa|Di)\b',
        "Numéros de semaine": r'\b(semaine|sem\.|n°|numéro|week)\s*(\d{1,2})\b',
        "Collecte": r'\b(collecte|ordures|déchets|ménagers|trier|jeter|emballages)\b',
        "Symboles spéciaux": r'[★✦⚫●▲■◆◼❖❉✱✲✴]',
    }

    print(f"\n[Patterns trouvés dans la page {page_num}]:")
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Prendre seulement les premiers matches pour éviter trop d'output
            sample = matches[:10] if len(matches) > 10 else matches
            print(f"  {pattern_name}: {len(matches)} matches (échantillon: {sample})")


def extract_calendar_sections(pdf_path):
    """
    Extrait spécifiquement les sections qui ressemblent à des calendriers
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            print("\n=== SECTIONS CALENDRIER ===")

            all_calendar_text = ""
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()

                # Chercher des sections avec des numéros (probablement des calendriers)
                lines = text.split('\n')
                calendar_lines = []

                for line in lines:
                    # Une ligne de calendrier contient souvent plusieurs nombres
                    numbers_in_line = re.findall(r'\b\d{1,2}\b', line)
                    if len(numbers_in_line) >= 5:  # Au moins 5 nombres (jours de la semaine)
                        calendar_lines.append(line)

                if calendar_lines:
                    print(f"\n--- Page {page_num} (lignes calendrier) ---")
                    for line in calendar_lines:
                        print(line)
                    all_calendar_text += "\n".join(calendar_lines) + "\n"

            return all_calendar_text

    except Exception as e:
        print(f"ERREUR: {e}")
        return ""


def get_raw_text_by_page(pdf_path):
    """
    Retourne le texte brut organisé par page
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            pages_text = {}
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                pages_text[page_num] = text

            return pages_text

    except Exception as e:
        print(f"ERREUR: {e}")
        return {}


# Fonction principale
if __name__ == "__main__":
    # Chemin vers votre PDF
    pdf_path = "data/6_CAL2026 +10000_jeuOM_lunTRI.pdf"

    print("Script pour analyser le contenu du PDF")
    print(f"Fichier analysé: {pdf_path}")
    print("-" * 60)

    # Choix de l'utilisateur
    print("\nOptions disponibles:")
    print("1. Afficher tout le contenu du PDF")
    print("2. Extraire seulement les sections calendrier")
    print("3. Obtenir le texte brut par page")

    choix = input("\nVotre choix (1-3): ").strip()

    if choix == "1":
        read_pdf_content(pdf_path)
    elif choix == "2":
        calendar_text = extract_calendar_sections(pdf_path)

        # Analyser le texte du calendrier
        if calendar_text:
            print("\n=== ANALYSE DU TEXTE CALENDRIER ===")

            # Chercher les numéros de semaine
            week_numbers = re.findall(r'^\s*(\d{1,2})\s+', calendar_text, re.MULTILINE)
            print(f"Numéros de semaine trouvés: {sorted(set(week_numbers))}")

            # Chercher des dates complètes
            dates = re.findall(r'\b(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\s+(\d{1,2})\b',
                               calendar_text)
            print(f"Lignes de dates trouvées: {len(dates)}")

    elif choix == "3":
        pages_text = get_raw_text_by_page(pdf_path)
        for page_num, text in pages_text.items():
            print(f"\n{'=' * 60}")
            print(f"PAGE {page_num} (texte brut)")
            print(f"{'=' * 60}")
            print(text[:2000])  # Afficher seulement les premiers 2000 caractères
    else:
        print("Choix invalide. Utilisation par défaut: option 1")
        read_pdf_content(pdf_path)
