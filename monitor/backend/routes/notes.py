from flask import Blueprint, jsonify
from monitor.backend.repositories import notes
from monitor.backend.rules import json_object, validate_note

blueprint = Blueprint("notes", __name__, url_prefix="/api/notes")


def missing():
    return jsonify(error="해당 관찰 메모를 찾을 수 없습니다."), 404


@blueprint.get("")
def index():
    return jsonify(notes=notes.list_notes())


@blueprint.get("/<int:note_id>")
def detail(note_id):
    note = notes.find_note(note_id)
    return jsonify(note=note) if note else missing()


@blueprint.post("")
def create():
    values, errors = validate_note(json_object())
    if errors:
        return jsonify(error="제목과 내용을 확인해 주세요.", fields=errors), 400
    return jsonify(note=notes.create_note(**values)), 201


@blueprint.put("/<int:note_id>")
def edit(note_id):
    if notes.find_note(note_id) is None:
        return missing()
    values, errors = validate_note(json_object())
    if errors:
        return jsonify(error="제목과 내용을 확인해 주세요.", fields=errors), 400
    note = notes.update_note(note_id, **values)
    return jsonify(note=note) if note else missing()


@blueprint.delete("/<int:note_id>")
def delete(note_id):
    note = notes.delete_note(note_id)
    return jsonify(deleted_id=note["id"]) if note else missing()
