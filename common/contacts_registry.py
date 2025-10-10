"""
[OK] Реестр реальных контактов для публикации проектов на GitHub.

Этот модуль предоставляет централизованное управление контактной информацией
для использования агентами при создании README файлов и публикации проектов.

Использование:
    from common.contacts_registry import get_contacts

    contacts = get_contacts("lazy_income_public")
    print(contacts.author_name)  # Nikita Solovey
"""

from dataclasses import dataclass
from typing import Optional, Dict, Literal


ProfileType = Literal[
    "lazy_income_public",
    "client_public",
    "client_private"
]


@dataclass
class ContactInfo:
    """
    Информация о контактах проекта.

    Attributes:
        author_name: Полное имя автора/разработчика
        author_email: Email для связи
        github_username: Username на GitHub (владелец репозитория)
        company: Название компании
        website: URL сайта компании/проекта
        instagram: URL Instagram профиля
        youtube: URL YouTube канала
        telegram: URL Telegram канала
        tiktok: URL TikTok аккаунта
        facebook: URL Facebook профиля/группы
        developed_by: Строка "Developed by" для клиентских проектов
        developer_url: URL разработчика для клиентских проектов
    """
    author_name: str
    author_email: str
    github_username: str
    company: str
    website: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    telegram: Optional[str] = None
    tiktok: Optional[str] = None
    facebook: Optional[str] = None
    developed_by: Optional[str] = None
    developer_url: Optional[str] = None

    def to_readme_section(self) -> str:
        """
        Генерирует секцию контактов для README.md.

        Returns:
            str: Markdown секция с контактами
        """
        sections = []

        sections.append("## Author")
        sections.append(f"**{self.author_name}**")
        sections.append(f"- Email: {self.author_email}")
        sections.append(f"- GitHub: [@{self.github_username}](https://github.com/{self.github_username})")

        if self.company:
            sections.append(f"- Company: {self.company}")

        if self.website:
            sections.append(f"- Website: [{self.website}]({self.website})")

        # Social media links
        social_links = []
        if self.instagram:
            social_links.append(f"[Instagram]({self.instagram})")
        if self.youtube:
            social_links.append(f"[YouTube]({self.youtube})")
        if self.telegram:
            social_links.append(f"[Telegram]({self.telegram})")
        if self.tiktok:
            social_links.append(f"[TikTok]({self.tiktok})")
        if self.facebook:
            social_links.append(f"[Facebook]({self.facebook})")

        if social_links:
            sections.append(f"- Follow: {' | '.join(social_links)}")

        # Developed by section for client projects
        if self.developed_by and self.developer_url:
            sections.append("")
            sections.append(f"*Developed by {self.developed_by}* | [{self.developer_url}]({self.developer_url})")

        return "\n".join(sections)


# Профили контактов
CONTACT_PROFILES: Dict[ProfileType, ContactInfo] = {
    # Проекты Lazy Income AI (публичные)
    "lazy_income_public": ContactInfo(
        author_name="Nikita Solovey",
        author_email="nikitasolovey1@gmail.com",
        github_username="LazyIncomeAI",  # Рекомендуется переименовать Lambertain -> LazyIncomeAI
        company="Lazy Income AI",
        website="https://lambertain.agency",  # Для ссылочной массы
        instagram="https://www.instagram.com/solovey_nikita",
        youtube="https://www.youtube.com/@LazyIncome_AI",
        telegram="https://t.me/LazyIncomeAI",
        tiktok="https://www.tiktok.com/@lazyincome_ai",
        facebook="https://www.facebook.com/profile.php?id=61573906928624"
    ),

    # Разработка для клиентов (публичный репозиторий клиента)
    "client_public": ContactInfo(
        author_name="Nikita Solovey",
        author_email="nikitasolovey1@gmail.com",
        github_username="[CLIENT_GITHUB_USERNAME]",  # Заменить на username клиента
        company="[CLIENT_COMPANY_NAME]",  # Заменить на название компании клиента
        website="[CLIENT_WEBSITE]",  # Заменить на сайт клиента
        developed_by="Nikita Solovey | Lazy Income AI",
        developer_url="https://github.com/LazyIncomeAI"
    ),

    # Разработка для клиентов (приватный репозиторий)
    "client_private": ContactInfo(
        author_name="Nikita Solovey",
        author_email="nikitasolovey1@gmail.com",
        github_username="[CLIENT_GITHUB_USERNAME]",  # Заменить на username клиента
        company="[CLIENT_COMPANY_NAME]",  # Заменить на название компании клиента
        website="[CLIENT_WEBSITE]"  # Заменить на сайт клиента (опционально)
    )
}


def get_contacts(profile: ProfileType = "lazy_income_public") -> ContactInfo:
    """
    Получить контактную информацию по профилю.

    Args:
        profile: Тип профиля контактов
            - "lazy_income_public": Проекты Lazy Income AI (публичные)
            - "client_public": Клиентские проекты (публичный репо)
            - "client_private": Клиентские проекты (приватный репо)

    Returns:
        ContactInfo: Объект с контактной информацией

    Raises:
        ValueError: Если указан неизвестный профиль

    Examples:
        >>> contacts = get_contacts("lazy_income_public")
        >>> print(contacts.author_name)
        Nikita Solovey

        >>> contacts = get_contacts("client_public")
        >>> readme_section = contacts.to_readme_section()
    """
    if profile not in CONTACT_PROFILES:
        raise ValueError(
            f"Unknown profile: {profile}. "
            f"Available profiles: {', '.join(CONTACT_PROFILES.keys())}"
        )

    return CONTACT_PROFILES[profile]


def update_client_profile(
    profile_type: Literal["client_public", "client_private"],
    github_username: str,
    company_name: str,
    website: Optional[str] = None
) -> ContactInfo:
    """
    Обновить профиль клиента с реальными данными.

    Используй эту функцию когда создаешь проект для конкретного клиента.

    Args:
        profile_type: Тип клиентского профиля
        github_username: GitHub username клиента
        company_name: Название компании клиента
        website: Сайт клиента (опционально)

    Returns:
        ContactInfo: Обновленный профиль контактов

    Examples:
        >>> client_contacts = update_client_profile(
        ...     profile_type="client_public",
        ...     github_username="ClientCorp",
        ...     company_name="Client Corporation",
        ...     website="https://clientcorp.com"
        ... )
        >>> print(client_contacts.github_username)
        ClientCorp
    """
    if profile_type not in ["client_public", "client_private"]:
        raise ValueError(
            f"Invalid profile_type: {profile_type}. "
            f"Must be 'client_public' or 'client_private'"
        )

    # Получаем базовый профиль
    base_profile = CONTACT_PROFILES[profile_type]

    # Создаем обновленную копию
    updated_profile = ContactInfo(
        author_name=base_profile.author_name,
        author_email=base_profile.author_email,
        github_username=github_username,
        company=company_name,
        website=website,
        developed_by=base_profile.developed_by,
        developer_url=base_profile.developer_url
    )

    return updated_profile


def get_git_config(profile: ProfileType = "lazy_income_public") -> Dict[str, str]:
    """
    Получить конфигурацию для git commit.

    Используй эту функцию для настройки git коммитов с правильными контактами.

    Args:
        profile: Тип профиля контактов

    Returns:
        Dict с user.name и user.email для git config

    Examples:
        >>> git_config = get_git_config("lazy_income_public")
        >>> print(git_config)
        {'user.name': 'Nikita Solovey', 'user.email': 'nikitasolovey1@gmail.com'}

        # Применить в git:
        # git config user.name "Nikita Solovey"
        # git config user.email "nikitasolovey1@gmail.com"
    """
    contacts = get_contacts(profile)

    return {
        "user.name": contacts.author_name,
        "user.email": contacts.author_email
    }


# Примеры использования для агентов
USAGE_EXAMPLES = """
# Пример 1: Создание README для своего проекта
from common.contacts_registry import get_contacts

contacts = get_contacts("lazy_income_public")
readme_section = contacts.to_readme_section()

# Добавь эту секцию в конец README.md
with open("README.md", "a") as f:
    f.write("\\n\\n")
    f.write(readme_section)


# Пример 2: Создание проекта для клиента
from common.contacts_registry import update_client_profile

client_contacts = update_client_profile(
    profile_type="client_public",
    github_username="ClientCompany",
    company_name="Client Company Inc.",
    website="https://clientcompany.com"
)

readme_section = client_contacts.to_readme_section()
# Результат будет включать "Developed by Nikita Solovey | Lazy Income AI"


# Пример 3: Настройка git для проекта
from common.contacts_registry import get_git_config
import subprocess

git_config = get_git_config("lazy_income_public")

subprocess.run(["git", "config", "user.name", git_config["user.name"]])
subprocess.run(["git", "config", "user.email", git_config["user.email"]])
"""


if __name__ == "__main__":
    # Тестирование модуля
    print("[OK] Contacts Registry Module")
    print("=" * 60)

    # Тест 1: Получение профиля Lazy Income AI
    print("\n[TEST] Profile: lazy_income_public")
    contacts = get_contacts("lazy_income_public")
    print(f"Author: {contacts.author_name}")
    print(f"Email: {contacts.author_email}")
    print(f"GitHub: @{contacts.github_username}")
    print(f"YouTube: {contacts.youtube}")

    # Тест 2: Генерация секции README
    print("\n[TEST] README Section Generation:")
    print("-" * 60)
    print(contacts.to_readme_section())

    # Тест 3: Git config
    print("\n[TEST] Git Configuration:")
    git_config = get_git_config()
    for key, value in git_config.items():
        print(f"git config {key} \"{value}\"")

    print("\n[OK] All tests passed!")
