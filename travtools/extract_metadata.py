import json
import re

def extract_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Milieux
    milieu_match = re.search(r'\{.*?"milieu":\s*\[(.*?)\].*?\}', content, re.DOTALL)
    if not milieu_match:
        print("Could not find milieu block")
        return None
    
    milieux_json = "{\"milieu\": [" + milieu_match.group(1) + "]}"
    milieux = json.loads(milieux_json)['milieu']

    # Find sector blocks
    # We find the start comment, e.g. /* Milieux 1105 sectors */
    # Then we find the next { and matching }
    result = {
        "milieux": milieux,
        "sectors": {}
    }

    milieu_headers = re.finditer(r'/\* Milieux (\d+) sectors.*?\*/', content)
    for match in milieu_headers:
        m_code = match.group(1)
        start_idx = match.end()
        
        # Find the first { after the header
        json_start = content.find('{', start_idx)
        if json_start == -1: continue
        
        # Simple brace counting to find the closing }
        brace_count = 0
        json_end = -1
        for i in range(json_start, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        
        if json_end != -1:
            json_str = content[json_start:json_end]
            try:
                data = json.loads(json_str)
                result["sectors"][f"M{m_code}"] = data["Sectors"]
            except Exception as e:
                print(f"Error parsing sectors for {m_code}: {e}")

    return result

if __name__ == "__main__":
    data = extract_data('c:/code/StarBright/temp.txt')
    if data:
        with open('c:/code/StarBright/travtools/traveller_map_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print("Successfully extracted data to traveller_map_data.json")
