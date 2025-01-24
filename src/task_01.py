import mmh3
from bitarray import bitarray


class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.array = bitarray(size)
        self.array.setall(0)

    def _hashes(self, item):
        return [mmh3.hash(item, seed) % self.size for seed in range(self.num_hashes)]

    def add(self, item):
        if not isinstance(item, str) or not item:
            raise ValueError("should be a non-empty string")
        for value in self._hashes(item):
            self.array[value] = 1

    def contains(self, item):
        if not isinstance(item, str) or not item:
            raise ValueError("should be a non-empty string")
        return all(self.array[hash_val] for hash_val in self._hashes(item))


def check_password_uniqueness(bloom_filter, passwords):
    if not isinstance(passwords, list):
        raise ValueError("should be a list of passwords")

    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password:
            results[password] = "не знайдений або невірний формат"
            continue
        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123",
                              "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
