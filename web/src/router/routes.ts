import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/Layout.vue'),
    children: [{ path: '/', component: () => import('pages/Index.vue') }],
  },

  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '/dashboard',
        component: () => import('pages/Dashboard.vue'),
      },
      {
        path: '/explorer',
        component: () => import('pages/ExplorerHome.vue'),
      },
      {
        path: '/explorer/transactions',
        component: () => import('pages/ExplorerTransaction.vue'),
      },
      {
        path: '/explorer/blocks',
        component: () => import('pages/ExplorerBlocks.vue'),
      },
      {
        path: '/explorer/account/:address',
        component: () => import('pages/ExplorerAccountDetails.vue'),
      },
      {
        path: '/explorer/block/:id(\\d+)',
        component: () => import('pages/ExplorerBlockDetails.vue'),
      },
      {
        path: '/explorer/transaction/:tx_hash',
        component: () => import('pages/ExplorerTransactionDetails.vue'),
      },
      {
        path: '/org/insert/',
        component: () => import('pages/InsertContextView.vue'),
      },
      {
        path: '/portfolio/:addressable?',
        component: () => import('pages/PortfolioView.vue'),
      },
      {
        path: '/user_info',
        component: () => import('pages/UserSettingView.vue'),
      },
    ],
  },

  { path: '/entry/:action(login|register)', component: () => import('pages/EntryForm.vue') },


  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
  },
];

export default routes;
