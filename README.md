# E-Commerce-Sys
[![Contributors][contributors-shield]][contributors-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

[![MIT License][license-shield]][license-url]

[![logo][logo]]
<!-- PROJECT LOGO -->
<p align="center">
  
  <h2 align="center">AlyaCom E-Commerece Website</h3>

  <p align="center">
    An E-Comerece website to buy or sell your products here
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
<summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
The System (“إلياكم”) that is an E-commerce website provides online products where seller or system administrator can put on the website to be bought by buyer through credit card or pay-pal with the selected currency.
User has his/her own profile through which he/she can buy/sell/browse products.
User can add products which he/she intend to pay later to wish-list.
System also suggests a recommended product based on the historical browsing of the user or based on his/her activity. System shows products with their price, name, image, and review.

[![Product Name Screen Shot][product-screenshot]](https://github.com/MostafaSamyFayez/E-Commerce-Sys)

### Built With

* [Django](https://www.djangoproject.com/)
* [Bootstrap](https://getbootstrap.com)
* [MySql](https://www.mysql.com/)
* [Python](https://www.python.org/)
* [JavaScript](https://www.javascript.com/)
* [HTML5](https://www.w3schools.com/html/)
* [Css 3](https://www.w3schools.com/css/)
* [PayPal Api](https://developer.paypal.com/demo/checkout/#/pattern/client)


<!-- GETTING STARTED -->
## Getting Started
First You Should Prepare Local environment to Run the project and install prerequisties pefore clone

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python
  ```sh
  https://www.python.org/downloads/
  ```

* Django
  ```sh
  python -m pip install Django
  ```
* MySql
  ```sh
    https://dev.mysql.com/downloads/mysql/
  ```
* Packeges
  ```sh
  pip install Pillow
  pip install django-img
  pip install django-currencies
  ```

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/MostafaSamyFayez/E-Commerce-Sys
   ```
2. MySql configrations
   ```sh
   Connection name: django_e_com
   Database name: e_com_db
   Password : e-com123456789
   ```
3. Navigate cmd to "E-Commerce-Sys\DjangoECom"
4. Run data base migration from cmd
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
4. Now you Can Run the server without errors
   ```sh
   python manage.py runserver
   ```
5. Configure groups from admin page
   ```sh
   1-Open localhost admin page "http://127.0.0.1:8000/admin"
   2-Login using superuser account created before
   3-Add Groups and currencies as shown below
   4-When adding dolar currency check Active, Base and Default boxes
   ```
.
[![groups][groups]]
.
[![currency][currency]]

6. You can use this paypal sandbox account in chekout
   ```sh
   email: sb-qxpfi4418020@personal.example.com
   password: 'ag1+Y<z
   ```
<!-- USAGE EXAMPLES -->
## Usage

_For user guide examples, please refer to the [Documentation](https://github.com/MostafaSamyFayez/E-Commerce-Sys)_

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the Alyacom License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Email - [alyacom@gmail.com](alyacom@gmail.com)

Project Link: [https://github.com/MostafaSamyFayez/E-Commerce-Sys](https://github.com/MostafaSamyFayez/E-Commerce-Sys)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/MostafaSamyFayez/E-Commerce-Sys/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/badge/license-Alyacom-blue
[license-url]: https://github.com/MostafaSamyFayez/E-Commerce-Sys
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://github.com/MostafaSamyFayez/E-Commerce-Sys
[product-screenshot]: images/screenshot.PNG
[logo]: images/logo.PNG
[groups]: images/groups.PNG
[currency]: images/currency.PNG
