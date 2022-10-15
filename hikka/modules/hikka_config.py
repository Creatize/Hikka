#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

import ast
import functools
from math import ceil
import typing

from telethon.tl.types import Message

from .. import loader, utils, translations
from ..inline.types import InlineCall

# Everywhere in this module, we use the following naming convention:
# `obj_type` of non-core module = False
# `obj_type` of core module = True
# `obj_type` of library = "library"


@loader.tds
class HikkaConfigMod(loader.Module):
    """Interactive configurator for Hikka Userbot"""

    strings = {
        "name": "HikkaConfig",
        "choose_core": "🎚 <b>Choose a category</b>",
        "configure": "🎚 <b>Choose a module to configure</b>",
        "configure_lib": "🪴 <b>Choose a library to configure</b>",
        "configuring_mod": (
            "🎚 <b>Choose config option for mod</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_lib": (
            "🪴 <b>Choose config option for library</b> <code>{}</code>\n\n<b>Current"
            " options:</b>\n\n{}"
        ),
        "configuring_option": (
            "🎚 <b>Configuring option </b><code>{}</code><b> of mod"
            " </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "🪴 <b>Configuring option </b><code>{}</code><b> of library"
            " </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>Default: {}</b>\n\n<b>Current:"
            " {}</b>\n\n{}"
        ),
        "option_saved": (
            "🎚 <b>Option </b><code>{}</code><b> of module </b><code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_saved_lib": (
            "🪴 <b>Option </b><code>{}</code><b> of library </b><code>{}</code><b>"
            " saved!</b>\n<b>Current: {}</b>"
        ),
        "option_reset": (
            "♻️ <b>Option </b><code>{}</code><b> of module </b><code>{}</code><b> has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "option_reset_lib": (
            "♻️ <b>Option </b><code>{}</code><b> of library </b><code>{}</code><b> has"
            " been reset to default</b>\n<b>Current: {}</b>"
        ),
        "args": "🚫 <b>You specified incorrect args</b>",
        "no_mod": "🚫 <b>Module doesn't exist</b>",
        "no_option": "🚫 <b>Configuration option doesn't exist</b>",
        "validation_error": "🚫 <b>You entered incorrect config value. \nError: {}</b>",
        "try_again": "🔁 Try again",
        "typehint": "🕵️ <b>Must be a{eng_art} {}</b>",
        "set": "set",
        "set_default_btn": "♻️ Reset default",
        "enter_value_btn": "✍️ Enter value",
        "enter_value_desc": "✍️ Enter new configuration value for this option",
        "add_item_desc": "✍️ Enter item to add",
        "remove_item_desc": "✍️ Enter item to remove",
        "back_btn": "👈 Back",
        "close_btn": "🔻 Close",
        "add_item_btn": "➕ Add item",
        "remove_item_btn": "➖ Remove item",
        "show_hidden": "🚸 Show value",
        "hide_value": "🔒 Hide value",
        "builtin": "🛰 Built-in",
        "external": "🛸 External",
        "libraries": "🪴 Libraries",
    }

    strings_ru = {
        "choose_core": "🎚 <b>Выбери категорию</b>",
        "configure": "🎚 <b>Выбери модуль для настройки</b>",
        "configure_lib": "🪴 <b>Выбери библиотеку для настройки</b>",
        "configuring_mod": (
            "🎚 <b>Выбери параметр для модуля</b> <code>{}</code>\n\n<b>Текущие"
            " настройки:</b>\n\n{}"
        ),
        "configuring_lib": (
            "🪴 <b>Выбери параметр для библиотеки</b> <code>{}</code>\n\n<b>Текущие"
            " настройки:</b>\n\n{}"
        ),
        "configuring_option": (
            "🎚 <b>Управление параметром </b><code>{}</code><b> модуля"
            " </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>Стандартное:"
            " {}</b>\n\n<b>Текущее: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "🪴 <b>Управление параметром </b><code>{}</code><b> библиотеки"
            " </b><code>{}</code>\n<i>ℹ️ {}</i>\n\n<b>Стандартное:"
            " {}</b>\n\n<b>Текущее: {}</b>\n\n{}"
        ),
        "option_saved": (
            "🎚 <b>Параметр </b><code>{}</code><b> модуля </b><code>{}</code><b>"
            " сохранен!</b>\n<b>Текущее: {}</b>"
        ),
        "option_saved_lib": (
            "🪴 <b>Параметр </b><code>{}</code><b> библиотеки </b><code>{}</code><b>"
            " сохранен!</b>\n<b>Текущее: {}</b>"
        ),
        "option_reset": (
            "♻️ <b>Параметр </b><code>{}</code><b> модуля </b><code>{}</code><b>"
            " сброшен до значения по умолчанию</b>\n<b>Текущее: {}</b>"
        ),
        "option_reset_lib": (
            "♻️ <b>Параметр </b><code>{}</code><b> библиотеки </b><code>{}</code><b>"
            " сброшен до значения по умолчанию</b>\n<b>Текущее: {}</b>"
        ),
        "_cls_doc": "Интерактивный конфигуратор Hikka",
        "args": "🚫 <b>Ты указал неверные аргументы</b>",
        "no_mod": "🚫 <b>Модуль не существует</b>",
        "no_option": "🚫 <b>У модуля нет такого значения конфига</b>",
        "validation_error": (
            "🚫 <b>Введено некорректное значение конфига. \nОшибка: {}</b>"
        ),
        "try_again": "🔁 Попробовать еще раз",
        "typehint": "🕵️ <b>Должно быть {}</b>",
        "set": "поставить",
        "set_default_btn": "♻️ Значение по умолчанию",
        "enter_value_btn": "✍️ Ввести значение",
        "enter_value_desc": "✍️ Введи новое значение этого параметра",
        "add_item_desc": "✍️ Введи элемент, который нужно добавить",
        "remove_item_desc": "✍️ Введи элемент, который нужно удалить",
        "back_btn": "👈 Назад",
        "close_btn": "🔻 Закрыть",
        "add_item_btn": "➕ Добавить элемент",
        "remove_item_btn": "➖ Удалить элемент",
        "show_hidden": "🚸 Показать значение",
        "hide_value": "🔒 Скрыть значение",
        "builtin": "🛰 Встроенные",
        "external": "🛸 Внешние",
        "libraries": "🪴 Библиотеки",
    }

    strings_de = {
        "choose_core": "🎚 <b>Wähle eine Kategorie</b>",
        "configure": "🎚 <b>Modul zum Konfigurieren auswählen</b>",
        "configure_lib": "🪴 <b>Wählen Sie eine zu konfigurierende Bibliothek aus</b>",
        "configuring_mod": (
            "🎚 <b>Wählen Sie einen Parameter für das Modul aus</b>"
            " <code>{}</code>\n\n<b>Aktuell Einstellungen:</b>\n\n{}"
        ),
        "configuring_lib": (
            "🪴 <b>Wählen Sie eine Option für die Bibliothek aus</b>"
            " <code>{}</code>\n\n<b>Aktuell Einstellungen:</b>\n\n{}"
        ),
        "configuring_option": (
            "🎚 <b>Option </b><code>{}</code><b> des Moduls </b><code>{}</code>"
            "<b> konfigurieren</b>\n<i>ℹ️ {}</i>\n\n<b>Standard: {}</b>\n\n<b>"
            "Aktuell: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "🪴 <b>Option </b><code>{}</code><b> der Bibliothek </b><code>{}</code>"
            "<b> konfigurieren</b>\n<i>ℹ️ {}</i>\n\n<b>Standard: {}</b>\n\n<b>"
            "Aktuell: {}</b>\n\n{}"
        ),
        "option_saved": (
            "🎚 <b>Option </b><code>{}</code><b> des Moduls </b><code>{}</code>"
            "<b> gespeichert!</b>\n<b>Aktuell: {}</b>"
        ),
        "option_saved_lib": (
            "🪴 <b>Option </b><code>{}</code><b> der Bibliothek </b><code>{}</code>"
            "<b> gespeichert!</b>\n<b>Aktuell: {}</b>"
        ),
        "option_reset": (
            "♻️ <b>Option </b><code>{}</code><b> des Moduls </b><code>{}</code>"
            "<b> auf den Standardwert zurückgesetzt</b>\n<b>Aktuell: {}</b>"
        ),
        "option_reset_lib": (
            "♻️ <b>Option </b><code>{}</code><b> der Bibliothek </b><code>{}</code>"
            "<b> auf den Standardwert zurückgesetzt</b>\n<b>Aktuell: {}</b>"
        ),
        "_cls_doc": "Interaktiver Konfigurator von Hikka",
        "args": "🚫 <b>Du hast falsche Argumente angegeben</b>",
        "no_mod": "🚫 <b>Modul existiert nicht</b>",
        "no_option": "🚫 <b>Modul hat keine solche Konfigurationsoption</b>",
        "validation_error": (
            "🚫 <b>Ungültiger Konfigurationswert eingegeben. \nFehler: {}</b>"
        ),
        "try_again": "🔁 Versuche es noch einmal",
        "typehint": "🕵️ <b>Sollte {} sein</b>",
        "set": "setzen",
        "set_default_btn": "♻️ Standardwert",
        "enter_value_btn": "✍️ Wert eingeben",
        "enter_value_desc": "✍️ Gib einen neuen Wert für diese Option ein",
        "add_item_desc": "✍️ Gib den hinzuzufügenden Eintrag ein",
        "remove_item_desc": "✍️ Gib den zu entfernenden Eintrag ein",
        "back_btn": "👈 Zurück",
        "close_btn": "🔻 Schließen",
        "add_item_btn": "➕ Element hinzufügen",
        "remove_item_btn": "➖ Element entfernen",
        "show_hidden": "🚸 Wert anzeigen",
        "hide_value": "🔒 Wert verbergen",
        "builtin": "🛰 Ingebaut",
        "external": "🛸 Extern",
        "libraries": "🪴 Bibliotheken",
    }

    strings_hi = {
        "choose_core": "🎚 <b>एक श्रेणी चुनें</b>",
        "configure": "🎚 <b>कॉन्फ़िगर करने के लिए एक मॉड्यूल चुनें</b>",
        "configure_lib": "🪴 <b>कॉन्फ़िगर करने के लिए लाइब्रेरी का चयन करें</b>",
        "configuring_mod": (
            "🎚 <b>मॉड्यूल के लिए एक पैरामीटर चुनें</b> <code>{}</code>\n\n<b>वर्तमान"
            " सेटिंग:</b>\n\n{}"
        ),
        "configuring_lib": (
            "🪴 <b>लाइब्रेरी के लिए एक विकल्प चुनें</b> <code>{}</code>\n\n<b>वर्तमान"
            " सेटिंग:</b>\n\n{}"
        ),
        "configuring_option": (
            "🎚 <b>विकल्प </b><code>{}</code><b> मॉड्यूल </b><code>{}</code>"
            "<b> कॉन्फ़िगर कर रहा है</b>\n<i>ℹ️ {}</i>\n\n<b>डिफ़ॉल्ट: {}</b>\n\n<b>"
            "वर्तमान: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "🪴 <b>विकल्प </b><code>{}</code><b> लाइब्रेरी </b><code>{}</code>"
            "<b> कॉन्फ़िगर कर रहा है</b>\n<i>ℹ️ {}</i>\n\n<b>डिफ़ॉल्ट: {}</b>\n\n<b>"
            "वर्तमान: {}</b>\n\n{}"
        ),
        "option_saved": (
            "🎚 <b>विकल्प </b><code>{}</code><b> मॉड्यूल </b><code>{}</code>"
            "<b> सहेजा गया!</b>\n<b>वर्तमान: {}</b>"
        ),
        "option_saved_lib": (
            "🪴 <b>विकल्प </b><code>{}</code><b> लाइब्रेरी </b><code>{}</code>"
            "<b> सहेजा गया!</b>\n<b>वर्तमान: {}</b>"
        ),
        "option_reset": (
            "♻️ <b>विकल्प </b><code>{}</code><b> मॉड्यूल </b><code>{}</code>"
            "<b> डिफ़ॉल्ट मान पर रीसेट कर दिया गया</b>\n<b>वर्तमान: {}</b>"
        ),
        "option_reset_lib": (
            "♻️ <b>विकल्प </b><code>{}</code><b> लाइब्रेरी </b><code>{}</code>"
            "<b> डिफ़ॉल्ट मान पर रीसेट कर दिया गया</b>\n<b>वर्तमान: {}</b>"
        ),
        "_cls_doc": "Hikka की इंटरैक्टिव कॉन्फ़िगरेशन",
        "args": "🚫 <b>आपने गलत तर्क प्रदान किए हैं</b>",
        "no_mod": "🚫 <b>मॉड्यूल मौजूद नहीं है</b>",
        "no_option": "🚫 <b>मॉड्यूल में ऐसा कोई विकल्प नहीं है</b>",
        "validation_error": (
            "🚫 <b>अमान्य कॉन्फ़िगरेशन मान दर्ज किया गया। \nत्रुटि: {}</b>"
        ),
        "try_again": "🔁 पुन: प्रयास करें",
        "typehint": "🕵️ <b>यह {} होना चाहिए</b>",
        "set": "सेट करें",
        "set_default_btn": "♻️ डिफ़ॉल्ट",
        "enter_value_btn": "✍️ मूल्य दर्ज करें",
        "remove_item_btn": "➖ आइटम हटाएं",
        "show_hidden": "🚸 मूल्य दिखाएं",
        "hide_value": "🔒 मूल्य छिपाएं",
        "builtin": "🛰 बिल्ट-इन",
        "external": "🛸 बाहरी",
        "libraries": "🪴 लाइब्रेरी",
        "close_btn": "🔻 बंद करें",
        "back_btn": "👈 पीछे",
    }

    strings_uz = {
        "choose_core": "🎚 <b>Kurum tanlang</b>",
        "configure": "🎚 <b>Sozlash uchun modulni tanlang</b>",
        "configure_lib": "🪴 <b>Sozlash uchun kutubxonani tanlang</b>",
        "configuring_mod": (
            "🎚 <b>Modul uchun parametrni tanlang</b> <code>{}</code>\n\n<b>Joriy"
            " sozlamalar:</b>\n\n{}"
        ),
        "configuring_lib": (
            "🪴 <b>Kutubxona uchun variantni tanlang</b> <code>{}</code>\n\n<b>Hozirgi"
            " sozlamalar:</b>\n\n{}"
        ),
        "configuring_option": (
            "🎚 <b>Modul </b><code>{}</code><b> sozlamasi </b><code>{}</code><b>"
            " konfiguratsiya qilinmoqda</b>\n<i>ℹ️ {}</i>\n\n<b>Default:"
            " {}</b>\n\n<b>Hozirgi: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "🪴 <b>Modul </b><code>{}</code><b> kutubxonasi sozlamasi"
            " </b><code>{}</code><b> konfiguratsiya qilinmoqda</b>\n<i>ℹ️"
            " {}</i>\n\n<b>Default: {}</b>\n\n<b>Hozirgi: {}</b>\n\n{}"
        ),
        "option_saved": (
            "🎚 <b>Modul </b><code>{}</code><b> sozlamasi saqlandi!</b>\n<b>Hozirgi:"
            " {}</b>"
        ),
        "option_saved_lib": (
            "🪴 <b>Modul </b><code>{}</code><b> kutubxonasi sozlamasi"
            " saqlandi!</b>\n<b>Hozirgi: {}</b>"
        ),
        "option_reset": (
            "♻️ <b>Modul </b><code>{}</code><b> sozlamasi standart qiymatga"
            " tiklandi</b>\n<b>Hozirgi: {}</b>"
        ),
        "option_reset_lib": (
            "♻️ <b>Modul </b><code>{}</code><b> kutubxonasi sozlamasi standart qiymatga"
            " tiklandi</b>\n<b>Hozirgi: {}</b>"
        ),
        "_cls_doc": "Hikka interaktiv konfiguratsiyasi",
        "args": "🚫 <b>Siz noto'g'ri ma'lumot kiritdingiz</b>",
        "no_mod": "🚫 <b>Modul mavjud emas</b>",
        "no_option": "🚫 <b>Modulda bunday sozlamalar mavjud emas</b>",
        "validation_error": (
            "🚫 <b>Noto'g'ri konfiguratsiya ma'lumotlari kiritildi. \nXatolik: {}</b>"
        ),
        "try_again": "🔁 Qayta urinib ko'ring",
        "typehint": "🕵️ <b>Buni {} bo'lishi kerak</b>",
        "set": "Sozlash",
        "set_default_btn": "♻️ Standart",
        "enter_value_btn": "✍️ Qiymat kiriting",
        "remove_item_btn": "➖ Elementni o'chirish",
        "show_hidden": "🚸 Qiymatni ko'rsatish",
        "hide_value": "🔒 Qiymatni yashirish",
        "builtin": "🛰 Ichki",
        "external": "🛸 Tashqi",
        "libraries": "🪴 Kutubxona",
        "close_btn": "🔻 Yopish",
        "back_btn": "👈 Orqaga",
    }

    strings_tr = {
        "choose_core": "🎚 <b>Bir kategori seçin</b>",
        "configure": "🎚 <b>Yapılandırılacak bir modül seçin</b>",
        "configure_lib": "🪴 <b>Yapılandırılacak bir kitaplık seçin</b>",
        "configuring_mod": (
            "🎚 <b>Modül için bir parametre seçin</b> <code>{}</code>\n\n<b>Mevcut"
            " ayarlar:</b>\n\n{}"
        ),
        "configuring_lib": (
            "🪴 <b>Kitaplık için bir seçenek belirleyin</b>"
            " <code>{}</code>\n\n<b>Geçerli ayarlar:</b>\n\n{}"
        ),
        "configuring_option": (
            "🎚 <b>Modül </b><code>{}</code><b> seçeneği </b><code>{}</code>"
            "<b> yapılandırılıyor</b>\n<i>ℹ️ {}</i>\n\n<b>Varsayılan: {}</b>\n\n<b>"
            "Şimdiki: {}</b>\n\n{}"
        ),
        "configuring_option_lib": (
            "🪴 <b>Modül </b><code>{}</code><b> kütüphanesi seçeneği </b><code>{}</code>"
            "<b> yapılandırılıyor</b>\n<i>ℹ️ {}</i>\n\n<b>Varsayılan: {}</b>\n\n<b>"
            "Şimdiki: {}</b>\n\n{}"
        ),
        "option_saved": (
            "🎚 <b>Modül </b><code>{}</code><b> seçeneği kaydedildi!</b>\n<b>Şimdiki:"
            " {}</b>"
        ),
        "option_saved_lib": (
            "🪴 <b>Modül </b><code>{}</code><b> kütüphanesi seçeneği"
            " kaydedildi!</b>\n<b>Şimdiki: {}</b>"
        ),
        "option_reset": (
            "♻️ <b>Modül </b><code>{}</code><b> seçeneği varsayılan değere"
            " sıfırlandı</b>\n<b>Şimdiki: {}</b>"
        ),
        "option_reset_lib": (
            "♻️ <b>Modül </b><code>{}</code><b> kütüphanesi seçeneği varsayılan değere"
            " sıfırlandı</b>\n<b>Şimdiki: {}</b>"
        ),
        "_cls_doc": "Hikka etkileşimli yapılandırması",
        "args": "🚫 <b>Yanlış argüman girdiniz</b>",
        "no_mod": "🚫 <b>Modül bulunamadı</b>",
        "no_option": "🚫 <b>Modülde böyle bir seçenek bulunamadı</b>",
        "validation_error": (
            "🚫 <b>Yanlış yapılandırma bilgileri girildi. \nHata: {}</b>"
        ),
        "try_again": "🔁 Tekrar deneyin",
        "typehint": "🕵️ <b>Bu {} olmalıdır</b>",
        "set": "Ayarla",
        "set_default_btn": "♻️ Varsayılan",
        "enter_value_btn": "✍️ Değer girin",
        "remove_item_btn": "➖ Öğeyi kaldır",
        "show_hidden": "🚸 Değeri göster",
        "hide_value": "🔒 Değeri gizle",
        "builtin": "🛰 Dahili",
        "external": "🛸 Harici",
        "libraries": "🪴 Kütüphane",
        "back_btn": "👈 Geri",
    }

    _row_size = 3
    _num_rows = 5

    @staticmethod
    def prep_value(value: typing.Any) -> typing.Any:
        if isinstance(value, str):
            return f"</b><code>{utils.escape_html(value.strip())}</code><b>"

        if isinstance(value, list) and value:
            return (
                "</b><code>[</code>\n    "
                + "\n    ".join(
                    [f"<code>{utils.escape_html(str(item))}</code>" for item in value]
                )
                + "\n<code>]</code><b>"
            )

        return f"</b><code>{utils.escape_html(value)}</code><b>"

    def hide_value(self, value: typing.Any) -> str:
        if isinstance(value, list) and value:
            return self.prep_value(["*" * len(str(i)) for i in value])

        return self.prep_value("*" * len(str(value)))

    async def inline__set_config(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__reset_default(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        mod_instance = self.lookup(mod)
        mod_instance.config[option] = mod_instance.config.getdef(option)

        await call.edit(
            self.strings(
                "option_reset" if isinstance(obj_type, bool) else "option_reset_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__set_bool(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        validator = self.lookup(mod).config._config[option].validator
        doc = utils.escape_html(
            next(
                (
                    validator.doc[lang]
                    for lang in self._db.get(translations.__name__, "lang", "en").split(
                        " "
                    )
                    if lang in validator.doc
                ),
                validator.doc["en"],
            )
        )

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                utils.escape_html(self.lookup(mod).config.getdoc(option)),
                self.prep_value(self.lookup(mod).config.getdef(option)),
                self.prep_value(self.lookup(mod).config[option])
                if not validator or validator.internal_id != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
                if doc
                else "",
            ),
            reply_markup=self._generate_bool_markup(mod, option, obj_type),
        )

        await call.answer("✅")

    def _generate_bool_markup(
        self,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                *(
                    [
                        {
                            "text": f"❌ {self.strings('set')} `False`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    else [
                        {
                            "text": f"✅ {self.strings('set')} `True`",
                            "callback": self.inline__set_bool,
                            "args": (mod, option, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                )
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__add_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            try:
                query = ast.literal_eval(query)
            except Exception:
                pass

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            self.lookup(mod).config[option] = self.lookup(mod).config[option] + query
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    async def inline__remove_item(
        self,
        call: InlineCall,
        query: str,
        mod: str,
        option: str,
        inline_message_id: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            try:
                query = ast.literal_eval(query)
            except Exception:
                pass

            if isinstance(query, (set, tuple)):
                query = list(query)

            if not isinstance(query, list):
                query = [query]

            query = list(map(str, query))

            old_config_len = len(self.lookup(mod).config[option])

            self.lookup(mod).config[option] = [
                i for i in self.lookup(mod).config[option] if str(i) not in query
            ]

            if old_config_len == len(self.lookup(mod).config[option]):
                raise loader.validators.ValidationError(
                    f"Nothing from passed value ({self.prep_value(query)}) is not in"
                    " target list"
                )
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not self.lookup(mod).config._config[option].validator
                or self.lookup(mod).config._config[option].validator.internal_id
                != "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
            inline_message_id=inline_message_id,
        )

    def _generate_series_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("remove_item_btn"),
                            "input": self.strings("remove_item_desc"),
                            "handler": self.inline__remove_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                        {
                            "text": self.strings("add_item_btn"),
                            "input": self.strings("add_item_desc"),
                            "handler": self.inline__add_item,
                            "args": (mod, option, call.inline_message_id),
                            "kwargs": {"obj_type": obj_type},
                        },
                    ]
                    if self.lookup(mod).config[option]
                    else []
                ),
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def _choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            self.lookup(mod).config[option] = value
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        validator = self.lookup(mod).config._config[option].validator

        await call.edit(
            self.strings(
                "option_saved" if isinstance(obj_type, bool) else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(self.lookup(mod).config[option])
                if not validator.internal_id == "Hidden"
                else self.hide_value(self.lookup(mod).config[option]),
            ),
            reply_markup=[
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

        await call.answer("✅")

    async def _multi_choice_set_value(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        value: bool,
        obj_type: typing.Union[bool, str] = False,
    ):
        try:
            if value in self.lookup(mod).config._config[option].value:
                self.lookup(mod).config._config[option].value.remove(value)
            else:
                self.lookup(mod).config._config[option].value += [value]

            self.lookup(mod).config.reload()
        except loader.validators.ValidationError as e:
            await call.edit(
                self.strings("validation_error").format(e.args[0]),
                reply_markup={
                    "text": self.strings("try_again"),
                    "callback": self.inline__configure_option,
                    "args": (mod, option),
                    "kwargs": {"obj_type": obj_type},
                },
            )
            return

        await self.inline__configure_option(call, mod, option, False, obj_type)
        await call.answer("✅")

    def _generate_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'☑️' if self.lookup(mod).config[option] == value else '🔘'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : 6
                if self.lookup(mod).config[option]
                != self.lookup(mod).config.getdef(option)
                else 7
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    def _generate_multi_choice_markup(
        self,
        call: InlineCall,
        mod: str,
        option: str,
        obj_type: typing.Union[bool, str] = False,
    ) -> list:
        possible_values = list(
            self.lookup(mod)
            .config._config[option]
            .validator.validate.keywords["possible_values"]
        )
        return [
            [
                {
                    "text": self.strings("enter_value_btn"),
                    "input": self.strings("enter_value_desc"),
                    "handler": self.inline__set_config,
                    "args": (mod, option, call.inline_message_id),
                    "kwargs": {"obj_type": obj_type},
                }
            ],
            *utils.chunks(
                [
                    {
                        "text": (
                            f"{'☑️' if value in self.lookup(mod).config[option] else '◻️'} "
                            f"{value if len(str(value)) < 20 else str(value)[:20]}"
                        ),
                        "callback": self._multi_choice_set_value,
                        "args": (mod, option, value, obj_type),
                    }
                    for value in possible_values
                ],
                2,
            )[
                : 6
                if self.lookup(mod).config[option]
                != self.lookup(mod).config.getdef(option)
                else 7
            ],
            [
                *(
                    [
                        {
                            "text": self.strings("set_default_btn"),
                            "callback": self.inline__reset_default,
                            "args": (mod, option),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                    if self.lookup(mod).config[option]
                    != self.lookup(mod).config.getdef(option)
                    else []
                )
            ],
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__configure,
                    "args": (mod,),
                    "kwargs": {"obj_type": obj_type},
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ],
        ]

    async def inline__configure_option(
        self,
        call: InlineCall,
        mod: str,
        config_opt: str,
        force_hidden: bool = False,
        obj_type: typing.Union[bool, str] = False,
    ):
        module = self.lookup(mod)
        args = [
            utils.escape_html(config_opt),
            utils.escape_html(mod),
            utils.escape_html(module.config.getdoc(config_opt)),
            self.prep_value(module.config.getdef(config_opt)),
            self.prep_value(module.config[config_opt])
            if not module.config._config[config_opt].validator
            or module.config._config[config_opt].validator.internal_id != "Hidden"
            or force_hidden
            else self.hide_value(module.config[config_opt]),
        ]

        if (
            module.config._config[config_opt].validator
            and module.config._config[config_opt].validator.internal_id == "Hidden"
        ):
            additonal_button_row = (
                [
                    [
                        {
                            "text": self.strings("hide_value"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, False),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
                if force_hidden
                else [
                    [
                        {
                            "text": self.strings("show_hidden"),
                            "callback": self.inline__configure_option,
                            "args": (mod, config_opt, True),
                            "kwargs": {"obj_type": obj_type},
                        }
                    ]
                ]
            )
        else:
            additonal_button_row = []

        try:
            validator = module.config._config[config_opt].validator
            doc = utils.escape_html(
                next(
                    (
                        validator.doc[lang]
                        for lang in self._db.get(
                            translations.__name__, "lang", "en"
                        ).split(" ")
                        if lang in validator.doc
                    ),
                    validator.doc["en"],
                )
            )
        except Exception:
            doc = None
            validator = None
            args += [""]
        else:
            args += [
                self.strings("typehint").format(
                    doc,
                    eng_art="n" if doc.lower().startswith(tuple("euioay")) else "",
                )
            ]
            if validator.internal_id == "Boolean":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_bool_markup(mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Series":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_series_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "Choice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_choice_markup(call, mod, config_opt, obj_type),
                )
                return

            if validator.internal_id == "MultiChoice":
                await call.edit(
                    self.strings(
                        "configuring_option"
                        if isinstance(obj_type, bool)
                        else "configuring_option_lib"
                    ).format(*args),
                    reply_markup=additonal_button_row
                    + self._generate_multi_choice_markup(
                        call, mod, config_opt, obj_type
                    ),
                )
                return

        await call.edit(
            self.strings(
                "configuring_option"
                if isinstance(obj_type, bool)
                else "configuring_option_lib"
            ).format(*args),
            reply_markup=additonal_button_row
            + [
                [
                    {
                        "text": self.strings("enter_value_btn"),
                        "input": self.strings("enter_value_desc"),
                        "handler": self.inline__set_config,
                        "args": (mod, config_opt, call.inline_message_id),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("set_default_btn"),
                        "callback": self.inline__reset_default,
                        "args": (mod, config_opt),
                        "kwargs": {"obj_type": obj_type},
                    }
                ],
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__configure,
                        "args": (mod,),
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ],
            ],
        )

    async def inline__configure(
        self,
        call: InlineCall,
        mod: str,
        obj_type: typing.Union[bool, str] = False,
    ):
        btns = [
            {
                "text": param,
                "callback": self.inline__configure_option,
                "args": (mod, param),
                "kwargs": {"obj_type": obj_type},
            }
            for param in self.lookup(mod).config
        ]

        await call.edit(
            self.strings(
                "configuring_mod" if isinstance(obj_type, bool) else "configuring_lib"
            ).format(
                utils.escape_html(mod),
                "\n".join(
                    [
                        f"▫️ <code>{utils.escape_html(key)}</code>: <b>{{}}</b>".format(
                            self.prep_value(value)
                            if (
                                not self.lookup(mod).config._config[key].validator
                                or self.lookup(mod)
                                .config._config[key]
                                .validator.internal_id
                                != "Hidden"
                            )
                            else self.hide_value(value)
                        )
                        for key, value in self.lookup(mod).config.items()
                    ]
                ),
            ),
            reply_markup=list(utils.chunks(btns, 2))
            + [
                [
                    {
                        "text": self.strings("back_btn"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": obj_type},
                    },
                    {"text": self.strings("close_btn"), "action": "close"},
                ]
            ],
        )

    async def inline__choose_category(self, call: typing.Union[Message, InlineCall]):
        await utils.answer(
            call,
            self.strings("choose_core"),
            reply_markup=[
                [
                    {
                        "text": self.strings("builtin"),
                        "callback": self.inline__global_config,
                        "kwargs": {"obj_type": True},
                    },
                    {
                        "text": self.strings("external"),
                        "callback": self.inline__global_config,
                    },
                ],
                *(
                    [
                        [
                            {
                                "text": self.strings("libraries"),
                                "callback": self.inline__global_config,
                                "kwargs": {"obj_type": "library"},
                            }
                        ]
                    ]
                    if self.allmodules.libraries
                    and any(hasattr(lib, "config") for lib in self.allmodules.libraries)
                    else []
                ),
                [{"text": self.strings("close_btn"), "action": "close"}],
            ],
        )

    async def inline__global_config(
        self,
        call: InlineCall,
        page: int = 0,
        obj_type: typing.Union[bool, str] = False,
    ):
        if isinstance(obj_type, bool):
            to_config = [
                mod.strings("name")
                for mod in self.allmodules.modules
                if hasattr(mod, "config")
                and callable(mod.strings)
                and (mod.__origin__.startswith("<core") or not obj_type)
                and (not mod.__origin__.startswith("<core") or obj_type)
            ]
        else:
            to_config = [
                lib.name for lib in self.allmodules.libraries if hasattr(lib, "config")
            ]

        to_config.sort()

        kb = []
        for mod_row in utils.chunks(
            to_config[
                page
                * self._num_rows
                * self._row_size : (page + 1)
                * self._num_rows
                * self._row_size
            ],
            3,
        ):
            row = [
                {
                    "text": btn,
                    "callback": self.inline__configure,
                    "args": (btn,),
                    "kwargs": {"obj_type": obj_type},
                }
                for btn in mod_row
            ]
            kb += [row]

        if len(to_config) > self._num_rows * self._row_size:
            kb += self.inline.build_pagination(
                callback=functools.partial(
                    self.inline__global_config, obj_type=obj_type
                ),
                total_pages=ceil(len(to_config) / (self._num_rows * self._row_size)),
                current_page=page + 1,
            )

        kb += [
            [
                {
                    "text": self.strings("back_btn"),
                    "callback": self.inline__choose_category,
                },
                {"text": self.strings("close_btn"), "action": "close"},
            ]
        ]

        await call.edit(
            self.strings(
                "configure" if isinstance(obj_type, bool) else "configure_lib"
            ),
            reply_markup=kb,
        )

    @loader.command(
        ru_doc="Настроить модули",
        de_doc="Konfiguriere Module",
        tr_doc="Modülleri yapılandır",
        hi_doc="मॉड्यूल कॉन्फ़िगर करें",
        uz_doc="Modullarni sozlash",
    )
    async def configcmd(self, message: Message):
        """Configure modules"""
        args = utils.get_args_raw(message)
        if self.lookup(args) and hasattr(self.lookup(args), "config"):
            form = await self.inline.form("🌘", message)
            mod = self.lookup(args)
            if isinstance(mod, loader.Library):
                type_ = "library"
            else:
                type_ = mod.__origin__.startswith("<core")

            await self.inline__configure(form, args, obj_type=type_)
            return

        await self.inline__choose_category(message)

    @loader.command(
        ru_doc=(
            "<модуль> <настройка> <значениеЮ - установить значение конфига для модуля"
        ),
        de_doc=(
            "<Modul> <Einstellung> <Wert> - Setze den Wert der Konfiguration für das"
            " Modul"
        ),
        tr_doc="<modül> <ayar> <değer> - Modül için yapılandırma değerini ayarla",
        hi_doc="<मॉड्यूल> <सेटिंग> <मान> - मॉड्यूल के लिए कॉन्फ़िगरेशन मान सेट करें",
        uz_doc="<modul> <sozlash> <qiymat> - modul uchun sozlash qiymatini o'rnatish",
    )
    async def fconfig(self, message: Message):
        """<module_name> <property_name> <config_value> - set the config value for the module
        """
        args = utils.get_args_raw(message).split(maxsplit=2)

        if len(args) < 3:
            await utils.answer(message, self.strings("args"))
            return

        mod, option, value = args

        instance = self.lookup(mod)
        if not instance:
            await utils.answer(message, self.strings("no_mod"))
            return

        if option not in instance.config:
            await utils.answer(message, self.strings("no_option"))
            return

        instance.config[option] = value
        await utils.answer(
            message,
            self.strings(
                "option_saved"
                if isinstance(instance, loader.Module)
                else "option_saved_lib"
            ).format(
                utils.escape_html(option),
                utils.escape_html(mod),
                self.prep_value(instance.config[option])
                if not instance.config._config[option].validator
                or instance.config._config[option].validator.internal_id != "Hidden"
                else self.hide_value(instance.config[option]),
            ),
        )
