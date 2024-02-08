if __name__ == "__main__":
    print(*[list(map(float, ln.split())) for ln in input().split('|')], sep='\n')
