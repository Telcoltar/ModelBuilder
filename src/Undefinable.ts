export type Undefinable<T> = T | undefined

export const map = <K, S>(a: Undefinable<K>, f: (value: K) => S): Undefinable<S> => {
    if (a !== undefined) {
        return f(a)
    }
    return undefined
}