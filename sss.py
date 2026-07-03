
import os

# Назва файлу, куди збережемо весь код
output_file = 'all_my_code.txt'

with open(output_file, 'w', encoding='utf-8') as outfile:
    # Проходимося по всіх папках проєкту
    for root, dirs, files in os.walk('.'):
        # Пропускаємо системні папки та віртуальне середовище
        if any(skip in root for skip in ['__pycache__', '.venv', 'venv', 'dist', 'build', '.git']):
            continue
            
        for file in files:
            # Беремо тільки файли з кодом
            if file.endswith(('.py', '.yaml', '.qss', '.spec')):
                filepath = os.path.join(root, file)
                
                # Записуємо гарний заголовок для кожного файлу
                outfile.write(f"\n\n{'='*60}\n")
                outfile.write(f"📁 ФАЙЛ: {filepath}\n")
                outfile.write(f"{'='*60}\n\n")
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Помилка читання файлу: {e}]\n")

print(f"✅ Готово! Весь твій код зібрано у файл: {output_file}")