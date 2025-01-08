import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatePaperworkComponent } from './create-paperwork.component';

describe('CreatePaperworkComponent', () => {
  let component: CreatePaperworkComponent;
  let fixture: ComponentFixture<CreatePaperworkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CreatePaperworkComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreatePaperworkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
