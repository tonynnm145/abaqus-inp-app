import pandas as pd

def process_inp_file(all_lines):
    node_lines = []
    in_node_section = False
    for line in all_lines:
        if "*Node" in line:
            in_node_section = True
            continue
        elif in_node_section and line.startswith("*"):
            break
        elif in_node_section:
            node_lines.append(line.strip())

    z_coords = []
    for line in node_lines:
        parts = line.split(",")
        if len(parts) >= 4:
            try:
                z = float(parts[3])
                z_coords.append(z)
            except ValueError:
                continue

    unique_z = sorted(set(z_coords))
    if not unique_z:
        return {"error": "Không trích được toạ độ z từ file .inp."}

    df = pd.DataFrame({
        "STT": range(1, len(unique_z)+1),
        "Toạ độ z": unique_z
    })

    return {
        "df": df,
        "calc_E_Ep": lambda df, k: calculate_E_and_Ep(df.copy(), k),
        "generate_modified_inp": lambda lines, Ep10: modify_inp_file(lines, Ep10)
    }


def calculate_E_and_Ep(df, k):
    Eb = 70e9
    Et = 380e9
    h = 0.1
    df[f'E_k={k}'] = Eb + (Et - Eb) * ((2 * df['Toạ độ z'] + h) / (2 * h)) ** k

    Ep = []
    for i in range(len(df) - 1):
        E1 = df.loc[i, f'E_k={k}']
        E2 = df.loc[i + 1, f'E_k={k}']
        Ep.append((4 * E1 + 4 * E2) / 8)
    Ep.append(Ep[-1])
    df[f'Ep_k={k}'] = Ep

    Ep10 = Ep[:10]
    return df, Ep10


def modify_inp_file(original_lines, Ep10):
    # Tìm elset Layer
    layer_elset_blocks = []
    capture = False
    for line in original_lines:
        if line.strip().upper().startswith("*ELSET") and "LAYER_1" in line.upper():
            capture = True
            layer_elset_blocks.append(line)
            continue
        if capture:
            if line.strip().startswith("*") and not line.upper().startswith("*ELSET"):
                capture = False
            else:
                layer_elset_blocks.append(line)

    # Tạo block vật liệu
    materials_block = []
    for i in range(10):
        materials_block.append(f"*Material, name=ALU{i+1}")
        materials_block.append("*Density")
        materials_block.append("2700.,")
        materials_block.append("*Elastic")
        materials_block.append(f" {Ep10[i]:.4e}, 0.33")

    # Chèn vào instance
    new_lines = []
    inside_instance = False
    buffer_instance = []

    i = 0
    while i < len(original_lines):
        line = original_lines[i]

        if line.strip().upper().startswith("*INSTANCE"):
            inside_instance = True
            buffer_instance = [line]
            i += 1
            continue

        if inside_instance:
            buffer_instance.append(line)

            if line.strip().upper().startswith("*ELSET") and "SET-1" in line.upper() and "GENERATE" in line.upper():
                i += 1
                buffer_instance.append(original_lines[i])
                buffer_instance.extend(layer_elset_blocks)

            if line.strip() == ",":
                for j in range(10):
                    buffer_instance.append(f"*Solid Section, elset=Layer_{j+1}, material=ALU{j+1}")

            if line.strip().upper().startswith("*END INSTANCE"):
                new_lines.extend(buffer_instance)
                inside_instance = False
                buffer_instance = []

            i += 1
            continue

        new_lines.append(line)
        i += 1

    result_lines = []
    materials_inserted = False
    for line in new_lines:
        result_lines.append(line)
        if "** MATERIALS" in line.upper() and not materials_inserted:
            result_lines.extend(materials_block)
            materials_inserted = True

    return "\n".join(result_lines)
