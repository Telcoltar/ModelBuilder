import {z, ZodTypeAny} from "zod"
import {BaseModel} from "../models/common";

type Nullable<K> = K | null

export class Option<T> {
  readonly is_some: boolean
  readonly value?: Nullable<T>

  constructor(init: {is_some: boolean, value?: Nullable<T>}) {
    this.value = init.value
    this.is_some = init.is_some
  }

  unwrap() {
    if (!this.is_some) {
      throw "Unwrap cant be called on None value"
    }
    return this.value as T
  }

  unwrap_or(default_value: T) {
    if (!this.is_some) {
      return default_value
    }
    return this.value as T
  }
}

export const None = new Option<never>({is_some: false, value: null})
export const Some = <T>(value: T) => {
  if (value === undefined || value === null) {
    throw "Value cant be undefined or null for Some"
  }
  return new Option({is_some: true, value: value})
}

type OptionType<IsComplex extends boolean, T extends BaseModel, K extends ZodTypeAny>
  = IsComplex extends true ? Option<T> : Option<z.infer<K>>

export const createOption = <IsComplex extends boolean, T extends BaseModel, K extends ZodTypeAny>(
  data: any,
  isComplex: IsComplex,
  modelType: IsComplex extends true ? {fromJSON: (parsedJSON: any) => T} : K
): OptionType<IsComplex, T, K> => {
  if (isComplex) {
    const {is_some, value} = OptionAnySchema.parse(data)
    const model = modelType as {fromJSON: (parsedJSON: any) => T}
    if (is_some) {
      return Some(model.fromJSON(value)) as OptionType<IsComplex, T, K>
    }
    return None as OptionType<IsComplex, T, K>
  } else {
    const zType = modelType as K
    const validated = createOptionSchema(zType).parse(data)
    return new Option<z.infer<K>>(validated) as OptionType<IsComplex, T, K>
  }
}

const OptionNoneSchema = z.object({
  is_some: z.literal(false),
  value: z.union([z.null(), z.undefined()])
})

const OptionAnySchema = z.union([
  OptionNoneSchema,
  z.object({
    is_some: z.literal(true),
    value: z.any()
  })
])

export const createOptionSchema = (z_type: z.ZodType) => (
  z.union([
    OptionNoneSchema,
    z.object({
      is_some: z.literal(true),
      value: z_type
    })
  ])
)