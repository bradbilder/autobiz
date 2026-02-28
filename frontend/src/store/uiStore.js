import { create } from 'zustand'

export const useUIStore = create((set, get) => ({
  // Modals
  activeModal: null,
  modalData: null,

  // Notifications
  notifications: [],

  // Loading states
  loadingStates: {},

  // Breadcrumbs
  breadcrumbs: [],

  openModal: (modalId, data = null) => {
    set({ activeModal: modalId, modalData: data })
  },

  closeModal: () => {
    set({ activeModal: null, modalData: null })
  },

  addNotification: (notification) => {
    const id = Date.now().toString()
    set((state) => ({
      notifications: [...state.notifications, { ...notification, id }],
    }))
    return id
  },

  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }))
  },

  setLoading: (key, isLoading) => {
    set((state) => ({
      loadingStates: { ...state.loadingStates, [key]: isLoading },
    }))
  },

  isLoading: (key) => {
    return !!get().loadingStates[key]
  },

  setBreadcrumbs: (breadcrumbs) => {
    set({ breadcrumbs })
  },
}))
