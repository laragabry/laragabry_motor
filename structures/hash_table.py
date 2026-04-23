class HashTable:
    def __init__(self, size=2048):
        self.size = size

        self.table = [[] for _ in range(size)]

        self.num_keys = 0

        self.collisions = 0

    def _hash(self, key):

        h = 5381


        for c in str(key):
            h = ((h << 5) + h) ^ ord(c)

        return h % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        bucket = self.table[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        if bucket:
            self.collisions += 1

        bucket.append((key, value))
        self.num_keys += 1

    def get(self, key):
        idx = self._hash(key)

        for k, v in self.table[idx]:
            if k == key:
                return v

        return None

    def contains(self, key):
        return self.get(key) is not None

    def delete(self, key):
        idx = self._hash(key)
        bucket = self.table[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i) 
                self.num_keys -= 1
                return True

        return False

    def items(self):
        for bucket in self.table:
            for k, v in bucket:
                yield k, v

    def keys(self):
        for k, _ in self.items():
            yield k

    def values(self):
        for _, v in self.items():
            yield v

    def load_factor(self):
        return self.num_keys / self.size

    def stats(self):
        used = sum(1 for b in self.table if b)

        maxlen = max((len(b) for b in self.table), default=0)

        return {
            "size": self.size,
            "keys": self.num_keys,
            "collisions": self.collisions,
            "load_factor": round(self.load_factor(), 4),
            "buckets_used": used,
            "max_chain": maxlen,
        }

    def __repr__(self):
        s = self.stats()
        return (f"HashTable(size={s['size']}, keys={s['keys']}, "
                f"load={s['load_factor']}, collisions={s['collisions']})")