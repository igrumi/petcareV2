var products = [
    {id: 1, name: '23', categoria: 'Perros', estado: 'Purina', stock: 'En Bodega', cantidad: '1'},
    {id: 2, name: '24', categoria: 'Gatos', estado: 'Hueso para perro', stock: 'Vendido', cantidad: '3'},
    {id: 3, name: '25', categoria: 'Perros', estado: 'Plato para mascota' ,stock: 'Entregado', cantidad: '2'}
  ];
  
  function findProduct (productId) {
    return products[findProductKey(productId)];
  };
  
  function findProductKey (productId) {
    for (var key = 0; key < products.length; key++) {
      if (products[key].id == productId) {
        return key;
      }
    }
  };
  
  var List = Vue.extend({
    template: '#product-list',
    data: function () {
      return {products: products, searchKey: ''};
    },
    computed: {
      filteredProducts: function () {
        return this.products.filter(function (product) {
          return this.searchKey=='' || product.name.indexOf(this.searchKey) !== -1;
        },this);
      }
    }
  });
  
  var Product = Vue.extend({
    template: '#product',
    data: function () {
      return {product: findProduct(this.$route.params.product_id)};
    }
  });
  
  var ProductEdit = Vue.extend({
    template: '#product-edit',
    data: function () {
      return {product: findProduct(this.$route.params.product_id)};
    },
    methods: {
      updateProduct: function () {
        var product = this.product;
        products[findProductKey(product.id)] = {
          id: product.id,
          name: product.name,
          categoria: product.categoria,
          estado: product.estado,
          stock: product.stock
        };
        router.push('/');
      }
    }
  });
  
  var ProductDelete = Vue.extend({
    template: '#product-delete',
    data: function () {
      return {product: findProduct(this.$route.params.product_id)};
    },
    methods: {
      deleteProduct: function () {
        products.splice(findProductKey(this.$route.params.product_id), 1);
        router.push('/');
      }
    }
  });
  
  var AddProduct = Vue.extend({
    template: '#add-product',
    data: function () {
      return {product: {name: '', categoria: '', estado: '', stock: '', cantidad: ''}}
    },
    methods: {
      createProduct: function() {
        var product = this.product;
        products.push({
          id: Math.random().toString().split('.')[1],
          name: product.name,
          categoria: product.categoria,
          estado: product.estado,
          stock: product.stock,
          cantidad: product.cantidad
        });
        router.push('/');
      }
    }
  });
  
  var router = new VueRouter({routes:[
    { path: '/', component: List},
    { path: '/product/:product_id', component: Product, name: 'product'},
    { path: '/add-product', component: AddProduct},
    { path: '/product/:product_id/edit', component: ProductEdit, name: 'product-edit'},
    { path: '/product/:product_id/delete', component: ProductDelete, name: 'product-delete'}
  ]});
  app = new Vue({
    router:router
  }).$mount('#app')