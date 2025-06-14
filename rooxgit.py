import os
import json
import base64
import requests
from InquirerPy import inquirer
from pyfiglet import figlet_format

# Banner (diperbaiki agar tidak ganda)
os.system("clear")
print("\033[92m")
print(figlet_format("ROOX GIT", font="slant"))
print("\033[0m")

# Load config
if not os.path.exists("config.json"):
    print("❌ File config.json tidak ditemukan!")
    print('Contoh isi config.json:\n{\n  "token": "your_github_token",\n  "username": "your_username"\n}')
    exit()

with open("config.json") as f:
    config = json.load(f)

token = config["token"]
username = config["username"]
headers = {"Authorization": f"token {token}"}

# Upload file
def upload_file_to_repo(file_path, repo, remote_path):
    if not os.path.exists(file_path):
        print(f"❌ File tidak ditemukan: {file_path}")
        return

    with open(file_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    url = f"https://api.github.com/repos/{username}/{repo}/contents/{remote_path}"
    message = f"Add {remote_path}"

    data = {"message": message, "content": content}
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [201, 200]:
        print(f"✅ Berhasil upload: {remote_path}")
    else:
        print(f"❌ Gagal upload {remote_path}: {response.json()}")

# Upload semua file dari folder lokal
def upload_folder_to_repo(folder_path, repo):
    if not os.path.isdir(folder_path):
        print("❌ Folder tidak ditemukan.")
        return

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            remote_path = os.path.relpath(file_path, folder_path)
            upload_file_to_repo(file_path, repo, remote_path)

# Buat repository baru
def create_repo():
    name = input("📁 Nama repo baru: ")
    desc = input("📝 Deskripsi repo: ")
    private = input("🔐 Private? (y/n): ").lower() == "y"

    data = {"name": name, "description": desc, "private": private}
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)

    if response.status_code == 201:
        print(f"✅ Repo '{name}' berhasil dibuat.")
        print(f"🔗 Link: https://github.com/{username}/{name}.git")
    else:
        print("❌ Gagal membuat repo:", response.json())

# Lihat daftar repo
def list_repos():
    response = requests.get(f"https://api.github.com/users/{username}/repos", headers=headers)
    if response.status_code == 200:
        print("\n📋 Daftar Repository:")
        for repo in response.json():
            print(f"🔹 {repo['name']} - {repo['html_url']}")
    else:
        print("❌ Gagal mengambil daftar repo:", response.json())

# Hapus repo
def delete_repo():
    name = input("🗑️ Nama repo yang ingin dihapus: ")
    confirm = input(f"⚠️ Yakin ingin menghapus '{name}'? (y/n): ").lower()
    if confirm != "y":
        print("❌ Dibatalkan.")
        return

    response = requests.delete(f"https://api.github.com/repos/{username}/{name}", headers=headers)
    if response.status_code == 204:
        print(f"✅ Repo '{name}' berhasil dihapus.")
    else:
        print("❌ Gagal menghapus repo:", response.json())

# Upload menu
def upload_file():
    repo = input("📦 Nama repo tujuan: ")
    opsi = inquirer.select(
        message="📤 Pilih metode upload:",
        choices=[
            "📄 Upload file lokal",
            "📁 Upload semua isi folder lokal",
            "❌ Batal"
        ]
    ).execute()

    if "file" in opsi:
        path = input("📄 Path file lokal: ")
        upload_file_to_repo(path, repo, os.path.basename(path))

    elif "folder" in opsi:
        folder = input("📁 Path folder lokal: ")
        upload_folder_to_repo(folder, repo)

    else:
        print("🚫 Upload dibatalkan.")

# Menu utama
def main():
    while True:
        menu = inquirer.select(
            message="📌 Pilih menu:",
            choices=[
                "📁 Buat Repository Baru",
                "📤 Upload File/Folder ke Repository",
                "📋 Lihat Daftar Repository",
                "🗑️ Hapus Repository",
                "❌ Keluar"
            ],
        ).execute()

        if "Buat Repository" in menu:
            create_repo()
        elif "Upload" in menu:
            upload_file()
        elif "Lihat Daftar" in menu:
            list_repos()
        elif "Hapus" in menu:
            delete_repo()
        elif "Keluar" in menu:
            print("👋 Keluar dari tools.")
            break

        input("\nTekan ENTER untuk kembali ke menu...")

if __name__ == "__main__":
    main()
