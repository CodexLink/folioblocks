import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/Layout.vue'),
    children: [{ path: '/', component: () => import('pages/Index.vue') }],
  },

  {
    path: '/dashboard',
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
        path: '/transactions',
        component: () => import('pages/ExplorerTransaction.vue'),
      },
      {
        path: '/explorerblocks',
        component: () => import('pages/ExplorerBlocks.vue'),
      },
      {
        path: '/exploreraccountdetails',
        component: () => import('pages/ExplorerAccountDetails.vue'),
      },
      {
        path: '/explorerblockdetails',
        component: () => import('pages/ExplorerBlockDetails.vue'),
      },
      {
        path: '/transaction/:tx_hash',
        component: () => import('pages/ExplorerTransactionDetails.vue'),
      },
      {
        path: '/insert',
        component: () => import('pages/Insert.vue'),
      },

      {
        path: '/view',
        component: () => import('pages/View.vue'),
      },
      {
        path: '/settings',
        component: () => import('pages/Setting.vue'),
      },
    ],
  },

  { path: '/entry/:action', component: () => import('pages/EntryForm.vue') },


  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue'),
  },
];

export default routes;
