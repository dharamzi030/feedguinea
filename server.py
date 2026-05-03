#!/usr/bin/env python3
"""
기니 밥주기 게임 서버
실행: python server.py  →  http://localhost:8000
"""
import http.server, socketserver, os, sys, mimetypes, urllib.parse

PORT = 8000

# .glb / .gltf MIME 타입 등록
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')

GLB_REL = os.path.join('guinea', 'guinea.glb')

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, fmt, *args):
        msg = fmt % args
        sys.stderr.write(f"  [{self.log_date_time_string()}] {msg}\n")

    def do_GET(self):
        decoded = urllib.parse.unquote(self.path)
        if decoded.endswith('.glb'):
            full = os.path.normpath(os.path.join(os.getcwd(), decoded.lstrip('/').lstrip('\\')))
            if os.path.exists(full):
                print(f"✅ GLB 서빙: {decoded} ({os.path.getsize(full):,} bytes)")
            else:
                print(f"❌ GLB 파일 없음: 요청={decoded}, 검색위치={full}")
        return super().do_GET()

def find_root():
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(os.path.join(here, GLB_REL)):
        return here
    parent = os.path.dirname(here)
    if os.path.exists(os.path.join(parent, GLB_REL)):
        return parent
    return here

if __name__ == '__main__':
    root = find_root()
    os.chdir(root)
    glb_path = os.path.join(root, GLB_REL)
    glb_ok = os.path.exists(glb_path)

    print(f"\n{'━'*50}")
    print(f"🐹 기니 밥주기 게임 서버")
    print(f"{'━'*50}")
    print(f"📁 서빙 폴더    : {root}")
    print(f"🐾 guinea.glb   : {'✅ 발견' if glb_ok else '❌ 없음!'}")
    if glb_ok:
        print(f"   파일 크기    : {os.path.getsize(glb_path):,} bytes")
        print(f"   전체 경로    : {glb_path}")
    print(f"🌐 접속 주소    : http://localhost:{PORT}")

    if not glb_ok:
        print(f"\n⚠️  '{GLB_REL}' 를 찾을 수 없습니다.")
        print(f"   현재 서빙 폴더 내용:")
        try:
            for f in sorted(os.listdir(root))[:30]:
                kind = 'DIR ' if os.path.isdir(os.path.join(root, f)) else 'FILE'
                print(f"     [{kind}] {f}")
        except Exception as e:
            print(f"   (목록 읽기 실패: {e})")

    print(f"\n⏹  종료: Ctrl+C")
    print(f"{'━'*50}\n")

    with socketserver.TCPServer(("", PORT), Handler) as srv:
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\n서버 종료!")
