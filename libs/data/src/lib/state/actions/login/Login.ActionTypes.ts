export const LOGIN_PENDING = 'LOGIN_PENDING'
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
export const LOGIN_FAILURE = 'LOGIN_FAILURE'

export interface LoginSuccessResponse {
  token: string
  username: string
}

export interface LoginFailureResponse {
  detail: string
}

export interface LoginPendingAction {
  type: typeof LOGIN_PENDING
}

export interface LoginSuccessAction {
  type: typeof LOGIN_SUCCESS
  payload: LoginSuccessResponse
}

export interface LoginFailureAction {
  type: typeof LOGIN_FAILURE
  payload: LoginFailureResponse
}

export type LoginActionTypes = LoginPendingAction | LoginSuccessAction | LoginFailureAction
