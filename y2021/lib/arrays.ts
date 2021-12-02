

export function list<TGen extends Iterator<TReturn>, TReturn>(gen: TGen): TReturn[] {
    let arr: TReturn[] = []
    let result = gen.next();
    while (!result.done) {
        arr.push(result.value)
        result = gen.next();
    }
    return arr
}

export function* zip<T1 extends any[], T2 extends any[]>(arr1: T1, arr2: T2): Iterator<[T1, T2]> {
    for (let i = 0; i < arr1.length; i++) {
        yield [arr1[i], arr2[i]]
    }
}