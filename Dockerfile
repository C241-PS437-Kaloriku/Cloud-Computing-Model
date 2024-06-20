# Gunakan base image resmi Python 3.9
FROM python:3.9-slim

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Salin requirements.txt ke direktori kerja
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install kembali dependencies Watchdog untuk menghindari error
RUN pip install --upgrade watchdog

# Salin seluruh kode aplikasi ke direktori kerja
COPY . .

# Insialasi Port
ENV PORT=5000

# Expose port yang akan digunakan oleh aplikasi
EXPOSE 5000

# Tentukan perintah untuk menjalankan aplikasi
CMD ["python3", "main.py"]
