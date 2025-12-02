import xml.etree.ElementTree as ET

file_path = r'c:\Users\kaganndemirr\tsn_simulation\debug_files\topology\ABB.graphml'

# Dosyayı oku
with open(file_path, 'r', encoding='UTF-8') as f:
    lines = f.readlines()

# Edge satırlarını bul ve oku
edges_data = []
for line in lines:
    if '<edge' in line and 'source=' in line:
        # source ve target değerlerini çıkar
        import re
        match = re.search(r'source="([^"]+)"\s+target="([^"]+)"', line)
        if match:
            edges_data.append((match.group(1), match.group(2)))

print(f"Bulunan edges: {len(edges_data)}")

# </graph> satırını bul
insert_index = -1
for i in range(len(lines) - 1, -1, -1):
    if '</graph>' in lines[i]:
        insert_index = i
        break

# Yeni edgeleri oluştur
new_edges_lines = []
max_id = 110
for source, target in edges_data:
    max_id += 1
    new_edge_line = f"        <edge source=\"{target}\" target=\"{source}\" id=\"e{max_id}\"><data key=\"d1\">1.0</data></edge>\n"
    new_edges_lines.append(new_edge_line)
    print(f"Eklendi: e{max_id} - source={target}, target={source}")

# Yeni edgeleri enjekte et
if insert_index > 0:
    lines = lines[:insert_index] + new_edges_lines + lines[insert_index:]

# Dosyaya yaz
with open(file_path, 'w', encoding='UTF-8') as f:
    f.writelines(lines)

print(f"\nDosya başarıyla güncellendi! Toplam {len(edges_data)} yeni edge eklendi.")
