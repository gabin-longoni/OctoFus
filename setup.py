from setuptools import setup, find_packages

setup(
    name='octofus',
    version='0.1.0',
    description='Une application de sniffeur de paquets avec interface graphique',
    author='Gabin  Longoni',
    author_email='gabin.longoni@gmail.com',
    url='https://github.com/votre_projet/my_application',  # Remplacez par l'URL de votre projet si applicable
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scapy',  # Exemple de dépendance pour le sniffing de paquets
        'PyQt5',  # Exemple de dépendance pour l'interface graphique
        # Ajoutez ici d'autres dépendances nécessaires
    ],
    entry_points={
        'console_scripts': [
            'run_sniffer=scripts.run_sniffer:main',
            'run_gui=scripts.run_gui:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
