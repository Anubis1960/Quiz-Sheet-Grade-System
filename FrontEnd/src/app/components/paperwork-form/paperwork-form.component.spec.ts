import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaperworkFormComponent } from './paperwork-form.component';

describe('PaperworkFormComponent', () => {
  let component: PaperworkFormComponent;
  let fixture: ComponentFixture<PaperworkFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PaperworkFormComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PaperworkFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
