import axios from 'axios'
import { Dispatch } from 'redux'
import { LoginActionTypes } from './Login.ActionTypes'

export const loginAction =
  (username: string, password: string) => async (dispatch: Dispatch<LoginActionTypes>) => {
    dispatch({
      type: 'LOGIN_PENDING'
    })

    try {
      const response = await axios.post(
        '/api/login',
        {
          username,
          password
        },
        { withCredentials: true }
      )

      dispatch({
        type: 'LOGIN_SUCCESS',
        payload: response.data
      })
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        dispatch({
          type: 'LOGIN_FAILURE',
          payload: error.response.data
        })
      } else {
        dispatch({
          type: 'LOGIN_FAILURE',
          payload: {
            detail: 'An unknown error occurred'
          }
        })
      }
    }
  }
