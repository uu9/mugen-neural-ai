import tensorflow as tf

def main():
    print("Hello from fight-ai!")
    print(tf.reduce_sum(tf.random.normal([1000, 1000])))


if __name__ == "__main__":
    main()
