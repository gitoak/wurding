describe('web-ui: WebUi component', () => {
  beforeEach(() => cy.visit('/iframe.html?id=webui--primary'));
    
    it('should render the component', () => {
      cy.get('h1').should('contain', 'Welcome to WebUi!');
    });
});
