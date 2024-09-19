# Function to identify the functional group and carbon count from the molecular structure
def get_functional_grp(structure):
    grp = "Unavailable"
    carbon_count = 0
    pos = ""
    use_pos = False

    # Special case for formic acid (HCOOH)
    if structure in ["HCOOH", "HCO2H"]:
        grp = "alkanoic acid"
        carbon_count = 1  # Formic acid has only 1 carbon atom
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # General hydrocarbon patterns: Alkanes, Alkenes, Alkynes
    hydro_carbon_match = structure.match(r'^C(\d*)H(\d+)$')
    if hydro_carbon_match:
        carbon_count = int(hydro_carbon_match[1] or '1')
        hydrogen_count = int(hydro_carbon_match[2])
        if hydrogen_count == 2 * carbon_count + 2:
            grp = "alkane"
        elif hydrogen_count == 2 * carbon_count:
            grp = "alkene"
        elif hydrogen_count == 2 * carbon_count - 2:
            grp = "alkyne"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Alcohols (Alkanols): CnH2n+1OH
    alkanol_match = structure.match(r'^C(\d*)H(\d+)OH$')
    if alkanol_match:
        carbon_count = int(alkanol_match[1] or '1')
        grp = "alkanol"
        if carbon_count > 2:
            pos = "1"  # Primary alcohol (OH group on the first carbon)
            use_pos = True
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    # Carboxylic Acids (Alkanoic Acids): CnH2n+1COOH or CnH2n+1CO2H
    alkanoic_acid_match = structure.match(r'^C(\d*)H(\d+)(COOH|CO2H)$')
    if alkanoic_acid_match:
        carbon_count = int(alkanoic_acid_match[1] or '1') + 1  # Add 1 for the carboxyl group (COOH)
        grp = "alkanoic acid"
        return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}

    return {"grp": grp, "carbonCount": carbon_count, "usePos": use_pos, "pos": pos}
