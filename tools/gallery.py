#!/usr/bin/env python3
"""Generate one gallery block for README and VitePress. Standard library only."""
import argparse
import html
import importlib.util
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/'
START = '<!-- logo-gallery:start -->'
END = '<!-- logo-gallery:end -->'
SKIP = {'docs', 'tools', 'web', 'blog', 'temp', 'node_modules', 'design', 'brand'}
TARGETS = ('README.md', 'docs/guide/logo-gallery.md')
spec = importlib.util.spec_from_file_location('check_brand', ROOT / 'tools/check-brand.py')
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


def entries(manifests=None):
    if manifests is None:
        manifests = contract.load_manifests()
    asset_dirs = {PurePosixPath(m['asset']).parts[0] for m in manifests}
    result = [(m['id'], m['asset'], m['darkAsset']) for m in manifests]
    for directory in sorted(ROOT.iterdir()):
        if not directory.is_dir() or directory.name.startswith('.') or directory.name in SKIP:
            continue
        if directory.name in asset_dirs:
            continue
        # Projects without a manifest use their current logo file.
        asset = next((directory / name for name in ('mark-v3.svg', 'logo-v2.svg', 'logo.svg', 'logo.png',
                     'logo.webp', 'icon.svg', 'logo-icon.webp', 'logo-icon.png')
                      if (directory / name).is_file()), None)
        if asset:
            dark = directory / 'mark-v3-dark.svg'
            if not dark.is_file():
                dark = directory / 'logo-dark.svg'
            result.append((directory.name, asset.relative_to(ROOT).as_posix(),
                           dark.relative_to(ROOT).as_posix() if dark.is_file() else None))
    return sorted(result)


def build(site_theme=False):
    manifests = contract.load_manifests()
    organizations = {m['id'] for m in manifests if m.get('kind') == 'organization'}
    preview_urls = {m['id']: m['galleryUrl'] for m in manifests if 'galleryUrl' in m}
    behavior = ('文档随站内主题开关显示对应 `darkAsset`（以根元素 `.dark` 为准）'
                if site_theme else '深色主题用 `<picture>` 按系统偏好加载对应 `darkAsset`')
    lines = [START, '', '## 🖼 项目 logo 墙', '',
             f'收录 GitHub 组织和项目的现役标识。{behavior}。', '']
    if site_theme:
        lines.extend(['<style>',
                      '.brand-gallery-dark { display: none !important; }',
                      '.dark .brand-gallery-light { display: none !important; }',
                      '.dark .brand-gallery-dark { display: inline-block !important; }',
                      '</style>', ''])
    organization_rows = []
    project_rows = []
    for id_, asset, dark in entries(manifests):
        preview_url = preview_urls.get(id_)
        source_url = html.escape(preview_url or BASE + asset)
        image = f'<img src="{source_url}" width="120" height="120" alt="{html.escape(id_)} logo">'
        if dark and not preview_url:
            if site_theme:
                image = image.replace('<img ', '<img class="brand-gallery-light" ', 1)
                image += f'<img class="brand-gallery-dark" src="{BASE}{html.escape(dark)}" width="120" height="120" alt="{html.escape(id_)} logo">'
            else:
                image = f'<picture><source media="(prefers-color-scheme: dark)" srcset="{BASE}{html.escape(dark)}">{image}</picture>'
        if id_ in organizations:
            organization_rows.append(f'| [{id_}](https://github.com/{id_}) | {image} | `{asset}` |')
        else:
            project_rows.append(f'| {id_} | {image} | `{asset}` |')
    if organization_rows:
        heading = '### GitHub 组织 {#github-organizations}' if site_theme else '### GitHub 组织'
        lines.extend([heading, '', '| 组织 | 标识 | 文件 |', '|---|---|---|', *organization_rows, ''])
    heading = '### 项目标识 {#project-logos}' if site_theme else '### 项目标识'
    lines.extend([heading, '', '| 项目 | 标识 | 文件 |', '|---|---|---|', *project_rows])
    lines.extend(['', END])
    return '\n'.join(lines)


def replace_block(text, block):
    if START not in text and END not in text:
        return text.rstrip() + '\n\n' + block + '\n'
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError('gallery markers must appear exactly once')
    before, rest = text.split(START)
    _, after = rest.split(END)
    return before + block + after


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name in TARGETS:
        block = build(site_theme=name.startswith('docs/'))
        path = ROOT / name
        current = path.read_text(encoding='utf-8')
        updated = replace_block(current, block)
        if args.check:
            if START not in current or updated != current:
                stale.append(name)
        elif updated != current:
            path.write_text(updated, encoding='utf-8')
    if stale:
        print('FAIL gallery stale: ' + ', '.join(stale) + '; run tools/gallery.sh')
        return 1
    print(('PASS gallery freshness' if args.check else 'PASS gallery generated')
          + ': README.md + docs/guide/logo-gallery.md; ' + str(len(entries())) + ' brands')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
