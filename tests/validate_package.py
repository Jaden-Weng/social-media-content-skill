"""Standard-library structural validation; does not evaluate model behavior."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[1]
entry = (root / 'SKILL.md').read_text(encoding='utf-8')
assert entry.startswith('---\n')
front = entry.split('---', 2)[1]
assert re.search(r'^name: employer-brand-content$', front, re.M)
assert re.search(r'^description: .+', front, re.M)
for path in root.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        if not link.startswith(('https://', 'http://', '#')):
            target = (path.parent / link.split('#')[0]).resolve()
            assert target.is_relative_to(root.resolve()), f'Outside root: {path}'
            assert target.exists(), f'Missing reference: {link}'
config = (root / 'agents/openai.yaml').read_text(encoding='utf-8')
assert config.startswith('interface:\n')
for line in config.splitlines()[1:]:
    assert re.fullmatch(r'  (display_name|short_description|default_prompt): "[^"\n]+"', line), 'Unexpected configuration'
assert '$employer-brand-content' in config
assets = list((root / 'assets').iterdir())
assert len(assets) == 1 and assets[0].name == 'demo-event-card.svg'
ET.parse(assets[0])
assert '虚构' in (root / 'references/simulated-example.md').read_text(encoding='utf-8')
print('PASS: manifest, local references, display configuration, original SVG and fictional example markers')
