from toc_search_utilities import TOCSearchEngine

def demo():
    engine = TOCSearchEngine("usb_pd_spec.jsonl")

    print("\n🔍 Search for 'Power':")
    for e in engine.search_by_keyword("Power")[:5]:
        print(f"{e['section_id']} {e['title']} (p.{e['page']})")

    print("\n📂 Level 2 Sections:")
    for e in engine.filter_by_level(2)[:5]:
        print(e['full_path'])

    print("\n📄 Page Range 50-60:")
    for e in engine.filter_by_page_range(50, 60):
        print(e['full_path'])

    print("\n🌳 Path for section '2.1.2':")
    for e in engine.get_path_to_root("2.1.2"):
        print(e['full_path'])

if __name__ == "__main__":
    demo()
