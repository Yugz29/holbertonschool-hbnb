import os

# Dossier racine du projet
base_dir = "part2"

# Structure à créer
structure = {
    "app": {
        "__init__.py": "",
        "api": {
            "__init__.py": "",
            "v1": {
                "__init__.py": "",
                "users.py": "",
                "places.py": "",
                "reviews.py": "",
                "amenities.py": "",
            }
        },
        "models": {
            "__init__.py": "",
            "user.py": "",
            "place.py": "",
            "review.py": "",
            "amenity.py": "",
        },
        "services": {
            "__init__.py": "",
            "facade.py": "",
        },
        "persistence": {
            "__init__.py": "",
            "repository.py": "",
        },
    },
    "run.py": "",
    "config.py": "",
    "requirements.txt": "",
    "README.md": "# HBnB Project\n\nGenerated project structure.\n",
}

def create_structure(base_path, struct):
    """Crée récursivement les dossiers et fichiers."""
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    create_structure(base_dir, structure)
    print(f"✅ Structure du projet '{base_dir}' créée avec succès !")